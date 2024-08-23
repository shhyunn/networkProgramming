
# Student ID : 2021310932, name: So-hyun Lim
# how to run : python local_server.py
# Import libraries
from socket import *
import cv2, struct, pickle
from datetime import datetime

# Define the local server name and port number
serverName = "127.0.0.1"
serverPort = 8000

# Create the server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)

print(f"HOST IP: {serverName}")
print(f"Listening at {(serverName, serverPort)}")

def find(videoname):
    with open("local_video.txt", "r") as file:
        for line in file:
            if line.strip() == videoname.strip():
                return 1
    return 0


def save_frames_to_mp4(frames, output_path, fps=20):
    with open("local_video.txt", "a") as file:
        file.write(f"{output_path.strip()}\n")
    output_path = output_path+".mp4"

    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()

while True:
    connectionSocket, addr = serverSocket.accept()
    print(addr)
    # Client랑 연결
    message = connectionSocket.recv(2048).decode()
    print(f"Request from client: {message}")
    print(f"CLIENT {addr} CONNECTED!")

    res = message.strip()
    if res == "video_2023":
        path = res + ".mp4"
        cap = cv2.VideoCapture(path)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 프레임 크기 조정
            frame = cv2.resize(frame, (320, 240))

            cv2.imshow("VIDEO IN LOCAL SERVER", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            text_size = cv2.getTextSize(timestamp, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            text_x = 10
            text_y = 30
            box_coords = ((text_x - 5, text_y + 5), (text_x + text_size[0] + 5, text_y - text_size[1] - 5))

            # 반투명한 빨간 배경 추가
            overlay = frame.copy()
            cv2.rectangle(overlay, box_coords[0], box_coords[1], (0, 0, 255), cv2.FILLED)
            alpha = 0.5  # 투명도 설정
            frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

            # 타임스탬프 텍스트 추가
            cv2.putText(frame, timestamp, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            data = pickle.dumps(frame)
            message_size = struct.pack("L", len(data))
            connectionSocket.sendall(message_size + data)

        cap.release()
        cv2.destroyAllWindows()

    else:
        #global server로 보내기, 고객 만들기
        globalServerName = "127.0.0.1"
        globalServerPort = 9000
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((globalServerName, globalServerPort))
        clientSocket.send(message.encode())

        # print(f"Request from client: {message}")
        # print(f"CLIENT {addr} CONNECTED!")
        data = b""
        payload_size = struct.calcsize("L")
        frames = []
        while True:
            while len(data) < payload_size:
                packet = clientSocket.recv(4096)
                if not packet:
                    break
                data += packet
            if len(data) < payload_size:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            # 전체 메시지 수신
            while len(data) < msg_size:
                data += clientSocket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # 수신한 데이터를 프레임으로 복원
            frame = pickle.loads(frame_data)

            # 프레임을 화면에 표시
            cv2.imshow('VIDEO IN LOCAL SERVER', frame)

            # 클라이언트로 프레임 전송
            data_to_send = pickle.dumps(frame)
            message_size = struct.pack("L", len(data_to_send))
            connectionSocket.sendall(message_size + data_to_send)
            frames.append(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if message.strip() != "live":
            save_frames_to_mp4(frames, message.strip())

        cap.release()
        cv2.destroyAllWindows()

    clientSocket.close()
    connectionSocket.close()

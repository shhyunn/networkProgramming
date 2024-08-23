# Student ID : 2021310932, name: So-hyun Lim
#how to run : python global_server.py
#import libraries
from socket import *
import cv2, struct, pickle
from datetime import datetime

#Define the global server name and port number
serverName = "127.0.0.1" 
serverPort = 9000

#Prepare a server socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((serverName, serverPort))
server_socket.listen(1)

print(f"HOST IP: {serverName}")
print(f"Listening at {(serverName, serverPort)}")

def find(videoname):
    with open("global_video.txt", "r") as file:
        for line in file:
            if line.strip() == videoname.strip():
                return 1
        
    return 0

time = 0
while True:
    connectionSocket, addr = server_socket.accept()
    time += 1
    if time == 1:
        print(f"CACHE SERVER {addr} CONNECTED!")

    message = connectionSocket.recv(2048) #GET /Result.html
    res = message.decode().strip()

    if res != "live":
        path = res + ".mp4"
        cap = cv2.VideoCapture(path)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 프레임 크기 조정
            frame = cv2.resize(frame, (320, 240))

            cv2.imshow("VIDEO IN GLOBAL SERVER", frame)
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
        # 라이브 비디오 스트리밍
        cap = cv2.VideoCapture(0)  # 웹캠으로부터 캡처 시작

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 프레임 크기 조정
            frame = cv2.resize(frame, (320, 240))

            cv2.imshow("LIVE STREAMING IN GLOBAL SERVER", frame)
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
    connectionSocket.close()
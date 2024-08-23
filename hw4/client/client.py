from socket import *
import cv2, struct, pickle

# Define the address and port number
serverName = "127.0.0.1"
serverPort = 8000

# Create the client socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

data = b""
payload_size = struct.calcsize("L")

message = input("Enter message: ")
clientSocket.send(message.encode())
print("Received video from cache server")

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
    cv2.imshow('VIDEO IN CLIENT', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the socket. The process terminates  
clientSocket.close()
cv2.destroyAllWindows()

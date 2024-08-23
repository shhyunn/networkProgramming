# Student ID : 2021310932, name: So-hyun Lim
#how to run : python global_server.py
#import libraries
import socket
import threading
import  struct

#Define the global server name and port number
serverName = "127.0.0.1"
serverPort = 9000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((serverName, serverPort))
server_socket.listen(5)

print(f"HOST IP: {serverName}")
print(f"Listening at {(serverName, serverPort)}")
print("global server is ready to receive")

def handle_client(connectionSocket, addr):
    message = connectionSocket.recv(2048) #GET /Result.html
    res = message.decode()

    if res.strip() == "video_2022":
        with open("./videos/video_2022.mp4", 'rb') as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                connectionSocket.sendall(bytes_read)

        connectionSocket.sendall(b"END")
        print(f"{res} sent at {addr}")

    #Text service
    if res.strip() == "Text":
        connectionSocket.send("Calculator asking expression: ".encode())
        message = connectionSocket.recv(2024)
        expression = message.decode()

        result = eval(expression)
        connectionSocket.send(f"Result: {result}".encode())
    
    #Image service
    if res.strip() == "sample":
        with open("./image/sample.jpg", 'rb') as f:
            image_data = f.read()

        img_name = connectionSocket.recv(1024)
        if img_name.decode() == 'sample':
            connectionSocket.send(struct.pack("L", len(image_data)))

            for i in range(0, len(image_data), 1024):
                connectionSocket.send(image_data[i:i+1024])

            print('Image sent to client.')

    connectionSocket.close()

while True:
    connectionSocket, addr = server_socket.accept()
    print(f"Connection attempt from {addr}")

    #threading for multi clients
    globalServer_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    globalServer_thread.start()

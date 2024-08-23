import socket, threading, struct

# login function
def handle_client_login(client_socket, client_address):
    attempts = 0

    #maximum value of login failure
    max_attempts = 3

    while attempts < max_attempts:
        try:
            client_socket.send(f"Please enter your ID".encode())
            message = client_socket.recv(buffer_size)
            print(f"{message.decode()} attemps for login.")

            #convert deximal id to binary id
            id = bin(int(message.decode()))[2:]


            with open('./ID_authen_binary.txt', 'r') as file:
                for _, line in enumerate(file, 1):
                    if id in line:
                        client_socket.send(f"{id} Login successful in from {client_address}".encode())
                        handle_client_expressions(client_socket, client_address)
                        return

            attempts += 1
            if attempts < max_attempts:
                client_socket.send(f"Login failed. Attempt {attempts}/{max_attempts}".encode())

            else:
                client_socket.send("Login failed. Maximum attempts reached.".encode())
                print(f"{id} failed to log in from {client_address}")
                return

        except Exception as e:
            print(f"Error in client handler: {e}")
            break

# expression function
def handle_client_expressions(client_socket, client_address):

    service = client_socket.recv(buffer_size).decode()

    if service.strip() == "Text":
        print(f"Request service from {client_address}: {service}")
        client_socket.send("Calculator asking expression: ".encode())

        message = client_socket.recv(buffer_size)
        expression = message.decode()

        #calculate expression
        result = eval(expression)

        #send the result of expression to client
        client_socket.send(f"Result: {result}".encode())
        handle_client_images(client_socket, client_address)

def handle_client_images(client_socket, client_address):
    with open("./image/sample.jpg", 'rb') as f:
        image_data = f.read()

    #receive image name
    img_name = client_socket.recv(1024)

    if img_name.decode() == 'sample':
        print('Image request received from', client_address)

        client_socket.send(struct.pack("L", len(image_data)))

        for i in range(0, len(image_data), 1024):
            client_socket.send(image_data[i:i+1024])

        print('Image sent to client.')

    handle_client_video(client_socket, client_address)

def handle_client_video(client_socket, client_address):
    video_name = client_socket.recv(1024).decode()
    print(f"{video_name} request received from {client_address}")

    if video_name.strip() == "video_2023":
        with open("./videos/video_2023.mp4", 'rb') as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)

        #send end flag to client
        client_socket.sendall(b"END")
        print(f'{video_name} sent to client.')
        handle_client_video2(client_socket, client_address)

def handle_client_video2(client_socket, client_address):
    video_name = client_socket.recv(1024)
    print(video_name.decode())
    
    if video_name.decode() == 'video_2022':
        #Define the global server name and port number
        globalServerName = "127.0.0.1"
        globalServerPort = 9000

        global_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        global_socket.connect((globalServerName, globalServerPort))

        global_socket.send(video_name)

        #store video data from global server
        with open("./videos/video_2022_from_global.mp4", 'wb') as f:
            while True:
                bytes_read = global_socket.recv(4096)
                if bytes_read == b"END":
                    break
                if not bytes_read:
                    break
                f.write(bytes_read)
        
        #send video data to client
        with open("./videos/video_2022_from_global.mp4", 'rb') as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)

        client_socket.sendall(b"END")
        print(f'{video_name} sent to client.')
        client_socket.close()

#Define the local server name and port number
buffer_size = 1024
serverName = '127.0.0.1'
serverPort = 8000
local_server_address = (serverName, serverPort)
local_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_server_socket.bind(local_server_address)
local_server_socket.listen(5)

print(f"HOST IP: {serverName}")
print(f"Listening at {(serverName, serverPort)}")
print("local server is ready to receive")

while True:
    client_socket, client_address = local_server_socket.accept()
    print(f"Connection attempt from {client_address}")

    #threading for multi clients
    client_thread = threading.Thread(target=handle_client_login, args=(client_socket, client_address))
    client_thread.start()
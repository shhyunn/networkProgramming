import socket, io, struct
from PIL import Image

#Define the client and port number
server_address = ('127.0.0.1', 8000)
buffer_size = 1024

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

#login function
def login():
    for _ in range(3):
        #input id from client and send id to local server
        id = input("Enter id: ").strip()
        client_socket.send(id.encode())

        #print login attempt results
        response = client_socket.recv(buffer_size)  
        response_message = response.decode()
        print(response_message)

        #in case of login success
        if "successful" in response_message: 
            return True

    return False

#text(calculator) function
def send_expression():
    #input service name from client and send service name to local server
    service = input("Request Service: ").strip()
    client_socket.send(service.encode())

    calculator = client_socket.recv(buffer_size).decode()

    #input expression from client and send expr to local server
    expression = input(calculator).strip()
    client_socket.send(expression.encode())

    #receive result and print
    response = client_socket.recv(buffer_size)
    print(f"Received expression result from server: {response.decode()}")

#image function
def send_image():
    #input image name from client and send image name to local server
    img_name = input("Enter image name: ").strip()
    client_socket.send(img_name.encode())


    #receive image data size
    data_size = struct.calcsize("L")
    data = client_socket.recv(data_size)
    image_size = struct.unpack("L", data)[0]
    image_data = b''

    #receive image data
    while len(image_data) < image_size:
        data = client_socket.recv(1024)
        if not data:
            break
        image_data += data

    # store jpg file
    with open("./result.jpg", 'wb') as f:
        f.write(image_data)
    print(f'{img_name} saved.')

    image = Image.open(io.BytesIO(image_data))
    image.show()
    print('Image received and displayed.')

#video(local) function
def send_video2023():
    #input video name (local) and send to server
    video_name = input("Enter video name (local): ").strip()
    client_socket.send(video_name.encode())
   
    #store video data
    with open("./video_2023_from_local.mp4", 'wb') as f:
        while True:
            bytes_read = client_socket.recv(4096)
            if bytes_read == b"END":
                break
            if not bytes_read:
                break
            f.write(bytes_read)

#video(global) function
def send_video2022():
    #input video name (global) and send to server
    video_name = input("Enter video name (global): ").strip()
    client_socket.send(video_name.encode())

    # store vieo data
    with open("./video_2022_from_global.mp4", 'wb') as f:
        while True:
            bytes_read = client_socket.recv(4096)
            if bytes_read == b"END":
                break
            if not bytes_read:
                break
            f.write(bytes_read)

try:
    # respone login requests
    response = client_socket.recv(buffer_size)

    if login():
        print("Logged in successfully.")
        send_expression()
        send_image()
        send_video2023()
        send_video2022()
    else:
        print("Failed to log in after 3 attempts.")

except KeyboardInterrupt:
    print("Client is shutting down.")
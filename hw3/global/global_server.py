# Student ID : 2021310932, name: So-hyun Lim
#how to run : python global_server.py
#import libraries
from socket import *

#Define the global server name and port number
serverName = "" 
serverPort = 9000

#Prepare a server socket
server_socket = socket(AF_INET, SOCK_STREAM)
# bind the socket to our global address
print("Waiting for clients to connect...")
server_socket.bind((serverName, serverPort))
server_socket.listen(1)

def find(domain):
    for filename in ['global_com_dns.txt', 'global_edu_dns.txt']:
        with open(filename, "r") as file:
            for line in file:
                words = line.split()
                if len(words) >= 2:
                    name, ip = words[0], words[1]
                    if name.strip() == domain.strip():
                        print(f"Received domain info: {name}")
                        return 1, ip
    return 0, ""

time = 0
while True:
    connectionSocket, addr = server_socket.accept()
    time += 1
    if time == 1:
        print("Client connected.")

    message = connectionSocket.recv(2048) #GET /Result.html
    print(f"Received packet from {addr[0]}:{addr[1]}")
    print(f"Data: {message.decode()}")
    res, ip = find(message.decode())

    if res == 1:
        connectionSocket.send(ip.encode())
        print(f"Sent IP address: {ip}")

    else:
        message = "Not Found"
        connectionSocket.send(message.encode())

    connectionSocket.close()
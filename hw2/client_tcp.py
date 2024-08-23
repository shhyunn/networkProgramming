# Student ID : 2021310932, name: So-hyun Lim
#how to run : python client_tcp.py
#Import libraries
from socket import *
import sys
#Define the address and port number
host = "172.30.64.1"
port = 12000
path = "/XYZ.html" 

#Create the client socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((host,port))

request = f"GET {path} HTTP/1.1"
clientSocket.send(request.encode())

response = ""
while True:
    data = clientSocket.recv(1024)
    if not data:
        break
    response += data.decode()

print(response)

#Close the socket. The process terminates  
clientSocket.close()
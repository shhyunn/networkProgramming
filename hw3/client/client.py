#use udp protocol
# Student ID : 2021310932, name: So-hyun Lim
#how to run : python client.py
#Import libraries
from socket import *

#Define the address and port number
serverName = "127.0.0.1"
serverPort = 8000

#Create the client socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

#Get domain name from the user then send to the server
with open('domain.txt', 'r') as file:
        domain_name = file.read()

#Send the domain name to the server
clientSocket.sendto(domain_name.encode(), (serverName, serverPort))

#Receive the answer from the server, print it, and save to the file name "result.txt"
#buffer size : 2048
result, serverAddress = clientSocket.recvfrom(2048)

#print answer
print(f"Result: {result.decode()}")
with open("result.txt", "w") as file:
    # write answer to "result.txt"
    file.write(result.decode())

#Close the socket. The process terminates  
clientSocket.close()
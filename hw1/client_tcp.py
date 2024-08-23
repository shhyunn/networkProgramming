# Student ID : 2021310932, name: So-hyun Lim
#how to run : python client_tcp.py
#Import libraries
from socket import *

#Define the address and port number
serverName = "127.0.0.1"
serverPort = 12000

#Create the client socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

#Get input from the user then send to the server
exp = input("Type the expression here: ")

#Send the expression to the server
clientSocket.send(exp.encode())

#Receive the answer from the server, print it, and save to the file name "result.txt"
#buffer size : 2048
calculated = clientSocket.recv(2048)
#print calculated answer
print(calculated.decode())
with open(".\\Result.txt", "w") as file:
    # write answer to "Result.txt"
    file.write(calculated.decode())

#Close the socket. The process terminates  
clientSocket.close()
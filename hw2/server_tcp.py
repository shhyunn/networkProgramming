# Student ID : 2021310932, name: So-hyun Lim
#how to run : python server_tcp.py
#import libraries
from socket import *
server_socket = socket(AF_INET, SOCK_STREAM)

#Prepare a server socket
#Define the server name and port number
serverName = "" 
serverPort = 12000
# bind the socket to our local address
server_socket.bind((serverName, serverPort))
server_socket.listen(1)

while True:
    #Establih the connection
    print('Ready to serve...')
    connectionSocket, addr = server_socket.accept()
    
    #Read expression from expression.txt file
    with open('expression.txt', 'r') as file:
        expr = file.read()
    #Solve expression in .txt file
    answer = eval(expr)

    #Save result to requestFile.html file
    html_content = f"<html><body><h1>{answer}</h1></body></html>"
    with open("Result.html", "w") as html_file:
        html_file.write(html_content)
    
    try:
        message = connectionSocket.recv(2048) #GET /Result.html
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        #Send one HTTP status line into socket
        header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
        connectionSocket.send(header.encode())
        
        #Send the content of the requested file to the client
        for i in range(0,len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
        print("OK!")

    except:
        #Send response message for file not found
        header = 'HTTP/1.1 404 Not Found\n\n'
        connectionSocket.send(header.encode())
        
        #Close client socket
        connectionSocket.close()
        print("OK!")
        
server_socket.close()
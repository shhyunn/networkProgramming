# Student ID : 2021310932, name: So-hyun Lim
#how to run : python server_udp.py
#import libraries
from socket import *

#Define the server name and port number
serverName = ""
serverPort = 12000

#Create the server socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# bind the socket to our local address
serverSocket.bind((serverName, serverPort))
print("The server is ready to receive.")

#Wait for an expression from client, calculate it, and send the answer to the client
def calculate(expr): #functions to calculate expression
    ans = 0 #initialize calculated answer
    i,l = 0, len(expr) #initialize index, length of expression
    
    while i < l: #loop for expression
        if expr[i] == "+": # + : add value to answer
            ans += int(expr[i+1])
            i += 2 # index is added two (operator, number)

        elif expr[i] == "-": # - : subtract value to answer
            ans -= int(expr[i+1])
            i += 2 #index is added two (operator, number)
        else:
            ans += int(expr[i]) #only number
            i += 1

    return ans #return calculated answer

try:
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        answer = calculate(message.decode())
        #after changing int to str, encodes calculated answer
        serverSocket.sendto(str(answer).encode(), clientAddress)

except KeyboardInterrupt:
    print("Press Ctrl-C to terminate while statement")
    pass
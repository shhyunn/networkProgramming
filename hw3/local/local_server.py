# Student ID : 2021310932, name: So-hyun Lim
#how to run : python local server.py
#import libraries
from socket import *

#Define the local server name and port number
serverName = ""
serverPort = 8000

#Create the server socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# bind the socket to our local address
serverSocket.bind((serverName, serverPort))
print("Bind successful. Wating for client input...")

def finds(domain):
    with open("local_dns.txt", "r") as file:
        for line in file:
            words = line.split()
            if len(words) >= 2:
                name, ip = words[0], words[1]
                if name.strip() == domain.strip():
                    print(f"Received domain: {name}")
                    return 1, ip
    return 0, ""

try:
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        print(f"Received packet from {clientAddress[0]}:{clientAddress[1]}")
        print(f"Data: {message.decode()}")
        res, ip = finds(message.decode())
        if res == 1:
            serverSocket.sendto(ip.encode(), clientAddress)
            print(f"Sent IP address: {ip}")

        else:
            #send to global dns server
            #Define the global server address and port number
            globalserverName = "127.0.0.1"
            globalserverPort = 9000

            #Create the client socket
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((globalserverName, globalserverPort))

            #Send the domain name to the server
            clientSocket.send(message)

            #buffer size : 2048
            globalResult = clientSocket.recv(2048)
            if globalResult.decode().strip() != "Not Found":
                with open("local_dns.txt", "a") as file:
                    # update answer to "local_dns.txt"
                    file.write(f"{message.decode().strip()} {globalResult.decode().strip()}\n")

            serverSocket.sendto(globalResult, clientAddress)
            print(f"IP from global DNS: {globalResult.decode()}")

            #Close the socket. The process terminates  
            clientSocket.close()
            

except KeyboardInterrupt:
    print("Press Ctrl-C to terminate while statement")
    pass
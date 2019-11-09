from socket import *
from _thread import *

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 5555
serverAddress =

serverSocket.bind(serverAddress, serverPort)
serverSocket.listen(20)
clientList = []

def userThread(connection, address):
    connection.send("This is the public chatroom")
    while True:
        try:
            message = connection.receive(1024)
            if message:
                #extract message content
                messageContent =
                #publish the message
                publish(messageContent, connection)
        except IOError: #remove user from chat room if there is no response
            if connection in clientList: clientList.remove(connection)
while True:
 #handle new connection = user
    connection, addr = serverSocket.accept()
    clientList.append(connection)
    start_new_thread(userThread,(connection,addr)) #create a new thread for each arriving connection

def publish(message, connection):
    for user in clientList:
        if user != connection:
            try:
                msgheader =
                message = msgheader + message
                user.send(message)
            except:
                user.close()
                clientList.remove(connection)

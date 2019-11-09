from socket import *
from _thread import *

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 5555
serverAddress =

serverSocket.bind(serverAddress, serverPort)
serverSocket.listen(20)
userList = []

def userThread(connection, address):
    connection.send("This is the public chatroom")
    while True:
        try:
            message = connection.receive(1024)
            if message:
                #extract message content
                messageContent =
                # publish the message
                publish(messageContent, connection)
        except IOError: #remove user from chat room
            if connection in userList: userList.remove(connection)
while True:
 #handle new connection = user
    connection, addr = serverSocket.accept()
    userList.append(connection)
    start_new_thread(userThread,(connection,addr)) #create a new thread for each arriving connection

def publish(message, connection):
    for client in userList:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                userList.remove(connection)

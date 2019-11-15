from socket import *
from _thread import *
from threading import *

CONNECTION_LIMIT = 10
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 5555
serverAddress = gethostbyname(gethostname())    #server ip

serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(20)

clientList = {}     #list of client (address,username)

#thread for handling one user connection
def userThread(connection, address, username):
    connection.send(("Welcome "+ username +", this is the public chatroom. Use '/signout' to exit. Type your message below\r\n------------").encode())
    cnnNotification = username+" ("+address[0]+") has joined the chat room"
    print(cnnNotification)
    publish(cnnNotification, connection, "[system]")
    while True:
        try:
            #waiting for client message
            message = connection.recv(1024).decode()
            print(message)
            if message:
                #extract message data
                message = message.split('\r\n')
                senderName = message[2].split()[1]
                messageContent = message[3].split(' ',1)[1]
                publish(messageContent, connection, senderName)
        except IOError:
            #remove user from chat room if there is an error/timeout
            if connection in clientList:
                disconnectMsg = clientList[connection]["username"] + " has disconnected!"
                print(disconnectMsg)
                publish(disconnectMsg, connection, "[system]")
                connection.close()
                del clientList[connection]


def publish(message, connection, username):
    for user in clientList:
        if user != connection:
        #if True:
            try:
                msgheader = "UNameL: 2\r\nMessageL: 4\r\nUsername: "+ username +"\r\nMessage: "+ message +"\r\n"
                user.send(msgheader.encode())
            except IOError:
                if user in clientList.keys():
                    del clientList[user]


#server establish new incoming connections
while True:
    connection, cAddress = serverSocket.accept()
    if len(clientList) >= CONNECTION_LIMIT:
        connection.send("Chat room is full at the moment, please try again later!".encode())
        connection.close()
        continue
    username = connection.recv(20).decode()
    clientList[connection] = {"username":username, "address": cAddress}
    #start_new_thread(userThread,(connection,cAddress)) #create a new thread for each arriving connection
    Thread(target=userThread, args=(connection, cAddress, username)).start()

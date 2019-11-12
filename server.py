from socket import *
from _thread import *
from threading import *

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 5555
serverAddress = gethostbyname(gethostname())    #server ip

serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(20)     #number of connections are allowed, enabled phase

clientList = {}     #list of client (address,username)

#thread for handling one user connection
def userThread(connection, address):
    connection.send(("Welcome "+ address[0] +", this is the public chatroom!").encode())
    print("<"+address[0]+"> connected")
    while True:
        try:
            #waiting for client message
            message = connection.recv(1024).decode()
            print(message)
            if message:
                #extract message data
                message = message.split('\r\n')
                username = message[2].split()[1]
                messageContent = message[3].split(' ',1)[1]
                publish(messageContent, connection, username)
        except IOError:
            #remove user from chat room if there is an error/timeout
            if connection in clientList:
                publish(clientList[connection] + " has disconnected!", connection, "system")
                connection.close()
                del clientList[connection]
                #clientList.remove(connection)

def publish(message, connection, username):
    for user in clientList:
        if user != connection:
        #if True:
            try:
                msgheader = "UNameL: 2\r\nMessageL: 4\r\nUsername: "+ username +"\r\nMessage: "+ message +"\r\n"
                user.send(msgheader.encode())
            except IOError:
                #clientList.remove(connection)
                break


#server establish new incoming connections
while True:
    connection, cAddress = serverSocket.accept()
    username = connection.recv(20).decode()
    #clientList.append(connection) #add new connection list
    clientList[connection] = username
    #start_new_thread(userThread,(connection,cAddress)) #create a new thread for each arriving connection
    Thread(target=userThread, args=(connection,cAddress)).start()

from socket import *
from _thread import *

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 5555
serverAddress = gethostbyname(gethostname())    #server ip

serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(20)     #number of connections are allowed, enabled phase

clientList = []     #list of client (address,username)

#thread for handling one user connection
def userThread(connection, address):
    connection.send(("Welcome "+ address[0] +", this is the public chatroom!").encode())
    while True:
        try:
            message = connection.recv(1024).decode()
            print(message)
            if message:
                #extract message data
                message = message.split('\r\n')
                username = message[2].split()[1]
                messageContent = message[3][9:]
                publish(messageContent, username)
        except IOError: #remove user from chat room if there is an error/timeout
            if connection in clientList:
                clientList.close()

def publish(message, connection):
    for user in clientList:
        # if user != connection:
        if True:
            try:
                msgheader = "UNameL: 2\r\nMessageL: 4\r\nUsername: "+ connection +"\r\nMessage: "+ message +"\r\n"
                user.send(msgheader.encode())
            except IOError:
                # user.close()
                clientList.remove(connection)

#server establish new incoming connections
while True:
    connection, cAddress = serverSocket.accept()
    clientList.append(connection) #add new connection list
    start_new_thread(userThread,(connection,cAddress)) #create a new thread for each arriving connection


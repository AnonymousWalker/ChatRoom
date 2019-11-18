from socket import *
from _thread import *
from threading import *

CONNECTION_LIMIT = 10
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 5555
serverAddress = gethostbyname(gethostname())  # server ip

serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(20)

clientList = {}  # list of client (address,username)


# thread for one user connection
def userThread(connection, address, senderName):
    pmUser = None
    while True:
        try:
            # waiting for client message
            message = connection.recv(1024).decode()
            print(message)
            if message:
                senderName, msgType, messageContent = extractMsgHeader(message)

                if msgType == 'cmd':
                    if messageContent == '/join':
                        clientList[connection]['isActive'] = True
                        connection.send(formatMessage('[system]',
                                                      "You have joined the public chatroom. Use '/esc' to exit. "
                                                      "Type your message below\r\n").encode())
                        notification = senderName + " (" + address[0] + ") has joined the chat room"
                        print(notification)
                        publish(notification, connection, "[system]")

                    elif messageContent == '/fetch':  # display active users
                        activeList = "Active users:\r\n"
                        for user in clientList:
                            if clientList[user]['isActive']:
                                activeList += clientList[user]['username'] + " (" + clientList[user]['ip'] + "/" + str(clientList[user]['port']) + ")\r\n"
                        connection.send(formatMessage('[system]', activeList).encode())

                    elif messageContent.startswith('/connect'):  # forward invitation
                        # clientList[connection]['isActive'] = False
                        messageContent = messageContent[1:].split('/')
                        ip = messageContent[1]
                        port = messageContent[2]

                        # find receiver in list
                        for conn in clientList:
                            #matching receiver
                            if clientList[conn]['ip'] == ip and clientList[conn]['port'] == int(port):
                                pmUser = (conn, clientList[conn]['username'])
                                forwdMsg = formatMessage('[system]',
                                                         senderName + "(" + address[0] + "/" + str(address[1]) + ") invited you to private "
                                                                                            "message.\r\nType "
                                                                                            "'/accept/ip/port' to accept.")
                                conn.send(forwdMsg.encode())
                                break

                    elif messageContent.startswith('/accept'):
                        messageContent = messageContent[1:].split('/')
                        ip = messageContent[1]
                        port = messageContent[2]

                        # find inviter
                        for conn in clientList:
                            if clientList[conn]['ip'] == ip and clientList[conn]['port'] == int(port):
                                clientList[conn]['isActive'] = False
                                clientList[connection]['isActive'] = False  # disable public msg
                                pmUser = (conn, clientList[conn]['username'])
                                forwdMsg = formatMessage('[system]', '/accept', 'cmd')
                                conn.send(forwdMsg.encode())
                                publish(senderName + " has left.", connection, '[system]')
                                #publish(clientList[conn]['username'] + " has left!", conn, '[system]')
                                break

                elif pmUser:
                    try:
                        pm = formatMessage(senderName, messageContent, 'pm')
                        pmUser[0].send(pm.encode())
                    except IOError:
                        pmUser = None
                        print(senderName+" couldn't connect to "+ pmUser[1])
                else:
                    publish(messageContent, connection, senderName)

        except IOError:
            # remove user from chat room if there is an error/timeout
            if connection in clientList:
                if clientList[connection]['isActive']:
                    disconnectMsg = clientList[connection]["username"] + " has disconnected!"
                    publish(disconnectMsg, connection, "[system]")
                print(disconnectMsg)
                del clientList[connection]


def publish(message, connection, username):
    for user in clientList:
        if user != connection and clientList[user]["isActive"]:
            try:
                msgheader = formatMessage(username, message)
                user.send(msgheader.encode())
            except IOError:
                if user in clientList.keys():
                    del clientList[user]


def formatMessage(username, message, msgType="msg"):
    return "UNameL: " + str(len(username)) + "\r\nMessageL: " + str(
        len(message)) + "\r\nMessageType: " + msgType + "\r\nUsername: " + username + "\r\nMessage: " + message


def extractMsgHeader(message):
    message = message.split('\r\n', 4)
    username = message[3].split()[1]
    messageType = message[2].split()[1]
    messageContent = message[4].split(' ', 1)[1]
    return (username, messageType, messageContent)


# server establish new incoming connections
while True:
    connection, cAddress = serverSocket.accept()

    # check room capacity
    if len(clientList) >= CONNECTION_LIMIT:
        msg = "Server is full at the moment, please try again later!"
        connection.send(format("[server]", msg).encode())
        connection.close()
        continue

    unameMsg = connection.recv(1024).decode()  # recv username
    username, type, content = extractMsgHeader(unameMsg)
    welcomeMsg = "Hi "+username+", welcome to chat server " + gethostname()
    connection.send(formatMessage("[server]", welcomeMsg).encode())

    clientList[connection] = {"username": username, "ip": cAddress[0], "port": cAddress[1], "isActive": False}
    # create a new thread for each arriving connection
    Thread(target=userThread, args=(connection, cAddress, username)).start()

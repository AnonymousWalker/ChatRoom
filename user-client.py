from socket import *
from threading import *
import os


def sizeof(data):
    return len(data.encode('utf-8'))


# thread to send msg
def sendMessage(sock):
    while True:
        messageToSend = input()
        if messageToSend == "/signout":
            sock.close()
            os._exit(1)
        uNameLen = sizeof(username)
        msgLen = sizeof(messageToSend)
        if msgLen > 4294967295: #msg max length is 4 bytes = 4,294,967,296
            print("(Error!) Your message is too long, plesase try again!")
            continue
        msgheader = "UNameL: "+str(uNameLen)+"\r\nMessageL: " + str(msgLen) + "\r\nUsername: " + username + "\r\nMessage: " + messageToSend + "\r\n"
        sock.send(msgheader.encode())


# thread to recv msg
def receiveMessage(sock):
    while True:
        try:
            message = sock.recv(1024).decode()  # wait for other message
        except IOError:
            print("You have been disconnected!")
            os._exit(1)
            break
        message = message.split('\r\n')
        senderName = message[2].split()[1]
        messageContent = message[3].split(' ', 1)[1]
        if senderName == '[system]':
            print("---" + messageContent + "---")
        else:
            print("<" + senderName + ">\t" + messageContent)


username = input("Please enter your username: ")
#Validate uname length: 2 bytes = 2^16 MAX
while sizeof(username) > 65535:
    username = input("Username is too long, please try again: ")
clientSocket = socket(AF_INET, SOCK_STREAM)
host = input("Enter the server address to connect: ")
port = input("Enter server port number: ")
clientSocket.connect((host, int(port)))
clientSocket.send(username.encode())
msg = clientSocket.recv(1024).decode()  # welcome message from server
print(msg)

Thread(target=sendMessage, args=(clientSocket,)).start()
Thread(target=receiveMessage, args=(clientSocket,)).start()

# def sendMessage(sock):
#     i=10
#     while (i > 0):
#         i = i - 1
#         try:
#             # send a message
#             messageToSend = input(str("Enter your message: "))
#             print("Me: " + messageToSend)
#             msgheader = "UNameL: 2\r\nMessageL: 4\r\nUsername: " + username + "\r\nMessage: " + messageToSend + "\r\n"
#             sock.send(msgheader.encode())
#         except IOError:
#             i=0
#             break
#             #clientSocket.close()
#
# def receiveMessage(sock):
#     i = 10
#     while (i>0):
#         try:
#             message = sock.recv(1024).decode()  # wait for other message
#             message.split('\r\n')
#             username = message[2].split()[1]
#             messageContent = message[3][9:]
#             print(username +": "+ messageContent)
#         except IOError:
#             i=0
#             break;
#
#
# start_new_thread(sendMessage, (clientSocket,))
# start_new_thread(receiveMessage, (clientSocket,))
#
#


# while i:
#     i -=1
#     try:
#         socketList = [sys.stdin, clientSocket]
#         #rsockets, wsockets, esockets = select.select(socketList, [], [])
#         read_sockets, write_socket, error_socket = select.select(socketList, [], [])
#         for s in read_sockets:
#             if s == clientSocket:
#             # extract message received from server
#                 msg = clientSocket.recv(1024).decode() #wait for other message
#                 print("Someone's message: " + msg)
#                 sys.stdout.flush()
#             else:
#             # send a message
#                 messageToSend = input(str("Enter your message: "))
#                 print("Me: " + messageToSend)
#                 sys.stdout.flush()
#                 msgheader = "UNameL: 2\r\nMessageL: 4\r\nUsername: " + username + "\r\nMessage: " + messageToSend + "\r\n"
#                 clientSocket.send(msgheader.encode())
#
#     except IOError:
#         clientSocket.close()

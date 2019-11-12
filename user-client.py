from socket import *
from threading import *

username = input("Please enter your username: ")

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('HoangAnh',5555))
clientSocket.send(username.encode())
msg = clientSocket.recv(1024).decode()  #welcome message from server
print(msg)

def sendMessage(sock):
    while True:
        messageToSend = input(str("Enter your message: "))
        print("Me: " + messageToSend)
        msgheader = "UNameL: 2\r\nMessageL: 4\r\nUsername: " + username + "\r\nMessage: " + messageToSend + "\r\n"
        sock.send(msgheader.encode())

def receiveMessage(sock):
    while True:
        message = sock.recv(1024).decode()  # wait for other message
        message= message.split('\r\n')
        senderName = message[2].split()[1]
        messageContent = message[3].split(' ',1)[1]
        print("<"+senderName + "> " + messageContent)

Thread(target=sendMessage, args=(clientSocket,)).start()
Thread(target=receiveMessage, args=(clientSocket,)).start()


# while True:
#     try:
#         sockets = [sys.stdin, clientSocket]
#         rsockets, wsockets, esockets =  select.select(sockets, [], [])
#         for socket in rsockets:
#             if socket == clientSocket:
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
#     except IOError:
#         clientSocket.close()

# def sendMessage():
#     while (i > 0):
#         i = i - 1
#         try:
#             # send a message
#             messageToSend = input(str("Enter your message: "))
#             print("Me: " + messageToSend)
#             msgheader = "UNameL: 2\r\nMessageL: 4\r\nUsername: " + username + "\r\nMessage: " + messageToSend + "\r\n"
#             clientSocket.send(msgheader.encode())
#         except IOError:
#             i=0
#             clientSocket.close()
#
# def receiveMessage():
#     while (i>0):
#         try:
#             message = clientSocket.recv(1024).decode()  # wait for other message
#             message = message.split('\r\n')
#             senderName = message[2].split()[1]
#             messageContent = message[3][9:]
#             print(username +": "+ messageContent)
#         except IOError:
#             clientSocket.close()
#             break;
#
# start_new_thread(receiveMessage)
# start_new_thread(sendMessage)


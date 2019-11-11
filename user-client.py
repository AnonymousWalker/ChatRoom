from socket import *
import sys
import select
i = 20
username = input(str("Please enter your username: "))
#messageContent = "I'm texting message body here..."

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('HoangAnh',5555))
msg = clientSocket.recv(1024).decode()  #welcome message from server
print(msg)

while True:
    try:
        sockets = [sys.stdin, clientSocket]
        rsockets, wsockets, esockets =  select.select(sockets, [], [])
        for socket in rsockets:
            if socket == clientSocket:
            # extract message received from server
                msg = clientSocket.recv(1024).decode() #wait for other message
                print("Someone's message: " + msg)
            else:
            # send a message
                messageToSend = input(str("Enter your message: "))
                print("Me: " + messageToSend)
                msgheader = "UNameL: 2\r\nMessageL: 4\r\nUsername: " + username + "\r\nMessage: " + messageToSend + "\r\n"
                clientSocket.send(msgheader.encode())

    except IOError:
        clientSocket.close()
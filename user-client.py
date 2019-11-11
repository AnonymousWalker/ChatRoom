from socket import *
from _thread import *
i = 20
username = input(str("Please enter your username: "))
#messageContent = "I'm texting message body here..."

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('HoangAnh',5555))
msg = clientSocket.recv(1024).decode()  #welcome message from server
print(msg)

def sendMessage():
    while (i > 0):
        i = i - 1
        try:
            # send a message
            messageToSend = input(str("Please enter your username: "))
            print("Me: " + messageToSend)
            msgheader = "UNameL: 2\r\nMessageL: 4\r\nUsername: " + username + "\r\nMessage: " + messageToSend + "\r\n"
            clientSocket.send(msgheader.encode())
        except IOError:
            i=0
            clientSocket.close()

def receiveMessage():
    while (i>0):
        try:
            message = clientSocket.recv(1024).decode()  # wait for other message
            message.split('\r\n')
            username = message[2].split()[1]
            messageContent = message[3][9:]
            print(username +": "+ messageContent)
        except IOError:
            clientSocket.close()
            break;

start_new_thread(receiveMessage)
start_new_thread(sendMessage)
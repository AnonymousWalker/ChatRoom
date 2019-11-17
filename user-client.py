from socket import *
from threading import *
import os


# thread to send msg
def sendMessage(sock):
    while True:
        messageToSend = input()
        if messageToSend == "/signout":
            sock.close()
            os._exit(1)
        if len(messageToSend) > 4294967295:  # msg max length is 4 bytes = 4,294,967,296
            print("(Error!) Your message is too long, plesase try again!")
            continue
        msgheader = formatMessage(username, messageToSend, 'cmd' if messageToSend.startswith('/') else 'msg')
        sock.send(msgheader.encode())


# thread to recv msg
def receiveMessage(sock):
    while True:
        try:
            message = sock.recv(1024).decode()  # wait for other message
            senderName, msgType, messageContent = extractMsgHeader(message)
            if senderName == '[system]':
                print("-------\r\n" + messageContent + "\r\n-------")
            else:
                print("[" + senderName + "]\t" + messageContent)
        except IOError:
            print("You have been disconnected!")
            os._exit(1)
            break


def formatMessage(username, message, msgType="msg"):
    return "UNameL: " + str(len(username)) + "\r\nMessageL: " + str(
        len(message)) + "\r\nMessageType: " + msgType + "\r\nUsername: " + username + "\r\nMessage: " + message


def extractMsgHeader(message):
    message = message.split('\r\n', 4)
    username = message[3].split()[1]
    messageType = message[2].split()[1]
    messageContent = message[4].split(' ', 1)[1]
    return (username, messageType, messageContent)


username = input("Please enter your username: ")
# Validate uname length: 2 bytes = 2^16 MAX
while len(username) > 65535:
    username = input("Username is too long, please try again: ")
clientSocket = socket(AF_INET, SOCK_STREAM)

host = input("Enter the server address to connect: ")
port = input("Enter server port number: ")
os.system('cls')
clientSocket.connect((host, int(port)))

unameMsg = formatMessage(username, username, 'cmd')
clientSocket.send(unameMsg.encode())

msg = clientSocket.recv(1024).decode()  # welcome message from server
welcomeMsg = msg.split('\r\n', 4)[4].split(' ', 1)[1]
print(welcomeMsg)
print(
    '>> Use the following command:\r\n\t/join : access public chatroom\r\n\t/fetch : see active users\r\n\t/connect/ip/port : invite user to private message\r\n\t/exit : close application.\r\n')

while True:
    cmd = input()
    if cmd.startswith('/'):
        if cmd == '/exit':
            clientSocket.close()
            os._exit(1)
        msg = formatMessage(username, cmd, "cmd")
        clientSocket.send(msg.encode())  # send command

        response = clientSocket.recv(1024).decode()  # recv server response
        sender, msgType, msgContent = extractMsgHeader(response)
        print(msgContent)
        if cmd == '/join':
            break
        # if cmd == '/fetch': #do nothing

        if cmd.startswith('/connect'):
            if msgContent.startswith('/accept'):  # start private message
                break

# join chatroom
Thread(target=sendMessage, args=(clientSocket,)).start()
Thread(target=receiveMessage, args=(clientSocket,)).start()

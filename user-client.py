from socket import *
from threading import *
import os


# thread to send msg
def sendMessage(sock):
    while True:
        messageToSend = input()
        if len(messageToSend) > 4294967295:  # msg max length is 4 bytes = 4,294,967,296
            print("(Error!) Your message is too long, plesase try again!")
            continue
        if messageToSend.startswith("/accept"):
            os.system('cls')
            print("You have join a private conversation. Type '/esc' to quit.")
        elif messageToSend == "/esc":
            sock.close()
            os._exit(1)
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

welcomeMsg = clientSocket.recv(1024).decode()  # welcome message from server
sender, type, welcome = extractMsgHeader(welcomeMsg)
print(welcome)
print(
    '>> Use the following command:\r\n\t/join : access public chatroom\r\n\t/fetch : see active users\r\n\t/connect/ip/port : invite user to private message\r\n\t/exit : close application.\r\n')

while True:
    cmd = input()
    if cmd.startswith('/'):
        if cmd == '/exit':
            clientSocket.close()
            os._exit(1)

        elif cmd == '/join':
            cmdMsg = formatMessage(username, cmd, "cmd")
            clientSocket.send(cmdMsg.encode())  # send command
            response = clientSocket.recv(1024).decode()  # recv active list
            sender, msgType, msgContent = extractMsgHeader(response)

            print(msgContent)
            break

        elif cmd == '/fetch':
            cmdMsg = formatMessage(username, cmd, "cmd")
            clientSocket.send(cmdMsg.encode())
            response = clientSocket.recv(1024).decode()  # recv active list
            sender, msgType, msgContent = extractMsgHeader(response)

            print(msgContent)
            continue

        elif cmd.startswith('/connect'):
            cmdMsg = formatMessage(username, cmd, "cmd")
            clientSocket.send(cmdMsg.encode())
            response = clientSocket.recv(1024).decode()
            sender, msgType, msgContent = extractMsgHeader(response)
            if msgContent.startswith('/accept'):  # reply from receiver
                os.system('cls')
                print("You have join a private conversation. Type '/esc' to quit.")
                break

# join chatroom
Thread(target=sendMessage, args=(clientSocket,)).start()
Thread(target=receiveMessage, args=(clientSocket,)).start()

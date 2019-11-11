from socket import *
i = 50
username = input(str("Please enter your username: "))
messageContent = "I'm texting message body here..."

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('HoangAnh',5555))
msg = clientSocket.recv(1024).decode()
print(msg)

while (i > 0):
    i = i - 1
    try:
        #send a message
        msgheader = "UNameL: 2\r\nMessageL: 4\r\nUsername: " + username + "\r\nMessage: " + messageContent + "\r\n"
        print("Me: "+ messageContent)
        clientSocket.send(msgheader.encode())

        # extract message received from server
        msg = clientSocket.recv(1024).decode() #wait for other message
        print("Someone's message: " + msg)
    except IOError:
        clientSocket.close()
from socket import *
i = 50
clientname = 'anonymous_client'
messageContent = "I'm texting message body here..."
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('HoangAnh',5555))
msg = clientSocket.recv(1024).decode()
print(msg)
while (i > 0):
    i = i - 1
    try:
        msgheader = "UNameL: 2\r\nMessageL: 4\r\nUsername: " + clientname + "\r\nMessage: "+messageContent+"\r\n"
        print("Me: "+ messageContent)
        clientSocket.send(msgheader.encode())
        msg = clientSocket.recv(1024).decode() #wait for other message
        print(msg)
    except IOError:
        clientSocket.close()
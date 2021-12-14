from socket import *

# Change to your host IP address
host = "127.0.0.1"
port = 8888

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(( host, port ))
serverSocket.listen(1)

while True:

    print("Ready to serve...")
    connectionSocket, addr = serverSocket.accept()

    try:
        msg = connectionSocket.recv(1024).decode()
        fileName = msg.split()[1]
        f = open(fileName[1:])
        outputData = f.read()
        f.close()

        outputData = 'HTTP/1.1 200 OK\r\n\r\n' + outputData
        connectionSocket.send(outputData.encode())
        # for i in range(0, len(outputData)):
        #     connectionSocket.send(outputData[i].encode())
        connectionSocket.close()

    except IOError:
        outputData = 'HTTP/1.1 404 NOT Found\r\n\r\n'
        for i in range(0, len(outputData)):
            connectionSocket.send(outputData[i].encode())
        connectionSocket.close()

serverSocket.close()

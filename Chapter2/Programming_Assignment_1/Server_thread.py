import threading
from socket import *

def response(connectionSocket):
        try:
            msg = connectionSocket.recv(1024).decode()
            fileName = msg.split()[1]
            f = open(fileName[1:])
            outputData = f.read()
            f.close()

            outputData = 'HTTP/1.1 200 OK\r\n\r\n' + outputData
            for i in range(0, len(outputData)):
                connectionSocket.send(outputData[i].encode())
            connectionSocket.close()

        except IOError:
            outputData = "HTTP/1.1 404 NOT Found\r\n\r\n"
            connectionSocket.send(outputData.encode())
            # for i in range(0, len(outputData)):
            #     connectionSocket.send(outputData[i].encode())
            connectionSocket.close()

if __name__ == "__main__":
    # Change to your host IP address
    host = "127.0.0.1"
    port = 8888

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen(5)

    while True:
        print("Ready to serve...")
        connectionSocket, addr = serverSocket.accept()
        thread = threading.Thread(target=response, args=(connectionSocket,))
        thread.start()

    serverSocket.close()

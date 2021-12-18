import re
import argparse
from socket import *

# Check arguments
def getArgs():
    # Get and parsing arguments
    parser = argparse.ArgumentParser(description='Send a GET method of HTTP request message to the specified port of the server to request the specified file')
    parser.add_argument('serverAddr', help='Server IP address: 127.0.0.1')
    # Convert serverPort(string) to int
    parser.add_argument('serverPort', type=int, help='port: 1~65535')
    args = parser.parse_args()

    # Check server IP address format
    pattern = re.compile('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
    serverAddr = pattern.match(args.serverAddr)
    if serverAddr is None:
        print('error: Server IP address is invaild!')
        exit(0)

    # Check server port
    if not( 1 <= args.serverPort <= 65535 ):
        print('error: Server port is invaild!')
        exit(0)

    return serverAddr.group(), args.serverPort

def serve(serverSocket):
    while True:

        print("Ready to serve...")
        connectionSocket, addr = serverSocket.accept()

        try:
            msg = connectionSocket.recv(1024).decode()
            fileName = msg.split()[1].partition('//')[2].partition('/')[2]
            print(fileName)
            f = open(fileName)
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

if __name__ == '__main__':
    serverAddr, serverPort = getArgs()

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(( serverAddr, serverPort ))
    serverSocket.listen(1)
    serve(serverSocket)

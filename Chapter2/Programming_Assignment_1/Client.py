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
    parser.add_argument('fileName', help='file path')
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

    return serverAddr.group(), args.serverPort,args.fileName


if __name__ == '__main__':
    # Init socket
    serverAddr, serverPort, fileName = getArgs()
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverAddr, serverPort))

    # send request and get response
    request = 'GET /' + fileName + ' HTTP/1.1\r\nHost: ' + serverAddr + '\r\n\r\n'
    clientSocket.send(request.encode())
    response = clientSocket.recv(1024).decode()
    clientSocket.close()

    print(response)

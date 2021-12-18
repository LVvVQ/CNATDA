import os
import re
import argparse
from socket import *

# Check arguments
def getArgs():
    # Get and parsing arguments
    parser = argparse.ArgumentParser(description='ProxyServer will forward the request to specify port of remote server')
    parser.add_argument('ProxyServerAddr', help='Proxy Server IP address: 127.0.0.1')
    # Convert serverPort(string) to int
    parser.add_argument('ProxyServerPort', type=int, help='port: 1~65535')
    parser.add_argument('RemoteServerPort', type=int, help='port: 1~65535')
    args = parser.parse_args()

    # Check server IP address format
    pattern = re.compile('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
    serverAddr = pattern.match(args.ProxyServerAddr)
    if serverAddr is None:
        print('error: Server IP address is invaild!')
        exit(0)

    # Check proxy server port
    if not( 1 <= args.ProxyServerPort <= 65535 ):
        print('error:Proxy server port is invaild!')
        exit(0)

    # Check remote server port
    if not( 1 <= args.RemoteServerPort <= 65535 ):
        print('error:Remote server port is invaild!')
        exit(0)
    return serverAddr.group(), args.ProxyServerPort,args.RemoteServerPort

def proxy(tcpSerSock, remoteServerPort):
    while 1:
        # Strat receiving data from the client
        print('Ready to serve:')
        tcpCliSock, cliAddr = tcpSerSock.accept()
        print('Received a connection from:' + cliAddr[0] )
        message = tcpCliSock.recv(2048).decode()
        print(message)
        # Extract the filename from the given message 
        fileName = message.split()[1].partition('//')[2]
        print('filename:' + fileName)
        fileExist = False
        try:
            # Check wether the file exist in the cache 
            with open('Cache/' + fileName, 'r') as f:
                outputData = f.read()
            fileExist = True
            # ProxyServer finds a cache hit and generates a response message 
            tcpCliSock.send(b'HTTP/1.1 200 OK\r\n')
            tcpCliSock.send(b'Content-Type: text/html\r\n\r\n')
            tcpCliSock.send(outputData.encode())
            print('Read from cache')

        except IOError:
            if not fileExist:
                # Create a socket on the proxyserver
                c = socket(AF_INET, SOCK_STREAM)
                hostn = fileName.replace("www.","",1).partition('/')[0]
                print('hostn:' + hostn)
                try:
                    # Connect to the socket to port 80 
                    c.connect((hostn, remoteServerPort))
                    # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    fileObj = c.makefile('rwb',0)
                    # POST method
                    if message.split()[0] == b'POST':
                        request = 'POST http://' + fileName + ' HTTP/1.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n\r\n'
                        fileObj.write(request.encode())
                        fileObj.write(message.split("\r\n\r\n")[1].encode())
                    # GET method
                    else:
                        request = 'GET http://' + fileName + ' HTTP/1.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n\r\n'
                        fileObj.write(request.encode())

                    # Read the response into buffer 
                    response = fileObj.read()
                    if response.split()[1] == b'404':
                        tcpCliSock.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
                        tcpCliSock.close()
                        continue

                    # Send the response in the buffer to client socket 
                    tcpCliSock.send(response)

                    # Create a new file in the cache for the requested file
                    if not os.path.exists('Cache/' + fileName):
                        dirName = os.path.split(fileName)
                        os.makedirs('Cache/' + dirName[0])
                    response = response.split(b'\r\n\r\n')[1]
                    tmpFile = open('Cache/' + fileName, 'wb')
                    tmpFile.write(response)
                    tmpFile.close()

                except:
                    print('Illegal request')

                c.close()
            else:
                # HTTP response message for file not found
                print('HTTP response message for file not found ')
        # Close the client and the server sockets
        tcpCliSock.close()
    tcpSerSock.close()

if __name__ == '__main__':
    # Create a server socket, bind it to a port and start listening 
    proxyServerAddr, proxyServerPort, remoteServerPort = getArgs()
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind((proxyServerAddr, proxyServerPort))
    tcpSerSock.listen(5)

    proxy(tcpSerSock, remoteServerPort)

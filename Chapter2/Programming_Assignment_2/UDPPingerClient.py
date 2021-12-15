import time
from socket import *

serverAddr = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

for i in range(1,11):
    try:
        msg = 'this is a test'
        start = time.perf_counter()
        clientSocket.sendto(msg.encode(), (serverAddr, serverPort))
        response, serverAddress = clientSocket.recvfrom(1024)
        end = time.perf_counter()
        print('Ping %d %fs' %(i, (end-start)))

    except timeout:
        print('Request time out')
        continue

clientSocket.close()

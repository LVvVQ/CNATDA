import time
from socket import *

serverAddr = '127.0.0.1'
serverPort = 12000
recvCount = 0
lossCount = 0
rtts = []
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

for i in range(1,11):
    try:
        msg = 'this is a test'
        start = time.perf_counter()
        clientSocket.sendto(msg.encode(), (serverAddr, serverPort))
        response, serverAddress = clientSocket.recvfrom(1024)
        end = time.perf_counter()
        rtt = end-start
        # Store each rtt into rtts[list]
        rtts.append(rtt)
        recvCount += 1
        print('Ping %d %fs' %(i, rtt))

    except timeout:
        lossCount += 1
        print('Request time out')
        continue

clientSocket.close()

print('\nPacket: Send = 10, Received = %d, loss = %d(%d%% loss)' %(recvCount, lossCount, lossCount*10, ))
print('Minimum = %fs Maximum = %fs Average = %fs' %(min(rtts), max(rtts), sum(rtts) / recvCount))

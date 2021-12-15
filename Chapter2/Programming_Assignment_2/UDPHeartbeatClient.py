import time
from socket import *

# Change your IP address
serverAddr = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Send packet sequence
seq = 1;

while True:
    msg = 'Ping ' + str(seq) + ' ' + str(time.perf_counter())
    clientSocket.sendto(msg.encode(), (serverAddr, serverPort))
    print(msg)
    seq += 1
    # Send heartbeat message every 2 seconds
    time.sleep(2)

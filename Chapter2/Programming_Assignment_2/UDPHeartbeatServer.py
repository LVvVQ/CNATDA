import time
from socket import *

serverAddr = '127.0.0.1'
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverAddr, serverPort))
# False = Offline, True = Oline
clientState = False
# Initially, client is offline, watting for the client online
serverSocket.settimeout(None)
# Recived packet sequence
seq = 0

while True:
    # Client oline
    if clientState:
        serverSocket.settimeout(6)

    try:
        msg, clientAddr = serverSocket.recvfrom(1024)
        recvTime = time.perf_counter()
        # msg format: Ping seq sendTime
        msg = msg.decode().split(' ')
        seq = int(msg[1])
        sendTime = float(msg[2])
        timeDiff = recvTime - sendTime

        # If client was offline before
        if not clientState:
            clientState = True
            print('\nClient online(%s)' %(clientAddr[0]))

        print('\tRecived packt %d, Time Difference = %fs' %(seq, timeDiff))

    # Packet lost->client offline
    # waitting for client to connect next time
    except timeout:
        clientState = False
        serverSocket.settimeout(None)
        print('No.%d packet lost, Client was offline.' %(seq+1))

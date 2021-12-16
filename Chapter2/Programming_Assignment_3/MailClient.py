import base64
from socket import *

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailServer = 'smtp.qq.com'
mailServerPort = 25
# FIXME: Change to your E-Mail username
username = '*********'
# FIXME: Change to your Authorization code
authCode = '*********'
# FIXME: Recipient mail
rcptToMail = '*********'

msg = '\r\n I love computer networks!'
endmsg = '\r\n.\r\n'

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, mailServerPort))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'Helo Alice\r\n'
clientSocket.send(heloCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send auth login command and print server response
authLogin = 'auth login\r\n'
clientSocket.send(authLogin.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '334':
    print('334 reply not received from server.')

# Send base64 encode of username and print server response
username64 = base64.b64encode(username.encode())
clientSocket.send(username64 + b'\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '334':
    print('334 reply not received from server.')

# Send base64 encode of Authorization code and print server response
authCode64 = base64.b64encode(authCode.encode())
clientSocket.send(authCode64 + b'\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '235':
    print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFrom = 'MAIL FROM: <' + username + '>\r\n'
clientSocket.send(mailFrom.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.  
rcptTo = 'RCPT TO: <' + rcptToMail + '>\r\n'
clientSocket.send(rcptTo.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.  
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '354':
    print('354 reply not received from server.')
 
# Send message data. 
clientSocket.send(msg.encode())

# Message ends with a single period. 
clientSocket.send(endmsg.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response. 
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '221':
    print('221 reply not received from server.')

clientSocket.close()

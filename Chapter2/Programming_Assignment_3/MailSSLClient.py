import ssl
import base64
from socket import *

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailServer = 'smtp.qq.com'
mailServerPort = 465
# FIXME: Change to your E-Mail username
username = '**********'
# FIXME: Change to your Authorization code
authCode = '**********'
# FIXME: Recipient mail
rcptToMail = '**********'

msg = '\r\n I love computer networks!'
endmsg = '\r\n.\r\n'

# Create socket called clientSocket and establish a TCP(SSL) connection with mailserver
context = ssl.create_default_context()
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, mailServerPort))
clientSocketSSL = context.wrap_socket(clientSocket, server_hostname=mailServer)

recv = clientSocketSSL.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'Helo Alice\r\n'
clientSocketSSL.send(heloCommand.encode())
recv = clientSocketSSL.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send auth login command and print server response
authLogin = 'auth login\r\n'
clientSocketSSL.send(authLogin.encode())
recv = clientSocketSSL.recv(1024).decode()
print(recv)
if recv[:3] != '334':
    print('334 reply not received from server.')

# Send base64 encode of username and print server response
username64 = base64.b64encode(username.encode())
clientSocketSSL.send(username64 + b'\r\n')
recv = clientSocketSSL.recv(1024).decode()
print(recv)
if recv[:3] != '334':
    print('334 reply not received from server.')

# Send base64 encode of Authorization code and print server response
authCode64 = base64.b64encode(authCode.encode())
clientSocketSSL.send(authCode64 + b'\r\n')
recv = clientSocketSSL.recv(1024).decode()
print(recv)
if recv[:3] != '235':
    print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFrom = 'MAIL FROM: <' + username + '>\r\n'
clientSocketSSL.send(mailFrom.encode())
recv = clientSocketSSL.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.  
rcptTo = 'RCPT TO: <' + rcptToMail + '>\r\n'
clientSocketSSL.send(rcptTo.encode())
recv = clientSocketSSL.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.  
dataCommand = 'DATA\r\n'
clientSocketSSL.send(dataCommand.encode())
recv = clientSocketSSL.recv(1024).decode()
print(recv)
if recv[:3] != '354':
    print('354 reply not received from server.')
 
# Send message data. 
clientSocketSSL.send(msg.encode())

# Message ends with a single period. 
clientSocketSSL.send(endmsg.encode())
recv = clientSocketSSL.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response. 
quitCommand = 'QUIT\r\n'
clientSocketSSL.send(quitCommand.encode())
recv = clientSocketSSL.recv(1024).decode()
print(recv)
if recv[:3] != '221':
    print('221 reply not received from server.')

clientSocketSSL.close()

'''
The main client script to send requests to the server
'''

import socket
from decouple import config

HOST = config("HOST")
PORT = config("PORT")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))
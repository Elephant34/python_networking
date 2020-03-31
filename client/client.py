'''
The main client script to send requests to the server
'''

import socket
from decouple import config

HOST = config("HOST")
PORT = config("PORT", cast=int)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        recieved_data = s.recv(1024)

        if not recieved_data:
            break
        else:
            print("Receieved: ", recieved_data.decode())

print("connection closed")
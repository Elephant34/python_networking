'''
The main server script which will recieve and handel requests
'''

import socket
from decouple import config

HOST = config("HOST")
PORT = config("PORT", cast=int)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
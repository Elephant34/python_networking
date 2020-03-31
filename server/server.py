'''
The main server script which will recieve and handel requests
'''

import socket
import threading
from time import sleep
from decouple import config

def client(conn, addr):
    '''
    Handels each client seperatly
    '''
    with conn:
        conn.sendall("Connected to server successfully".encode("utf-8"))
        sleep(10)
        conn.sendall("after a while hello again".encode("utf-8"))

HOST = config("HOST")
PORT = config("PORT", cast=int)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)

    while True:
        conn, addr = s.accept()

        print("Connection made with: ", addr)
        threading.Thread(target=client, args=(conn, addr)).start()


    
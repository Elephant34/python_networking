'''
The main server script which will recieve and handel requests
'''
import os
import socket
import threading
from time import sleep

from decouple import config


class Client:
    '''
    A client object to handel multithreading
    '''

    global client_list

    def __init__(self, conn, addr):
        '''
        Sets up the client and sends an alive message
        '''
        self.conn = conn
        self.addr = addr

        client_list.append(self)

        print("Connection made with: ", addr)

        with self.conn:
            self.conn.sendall("Connected to server successfully".encode("utf-8"))
            sleep(1)
            self.conn.sendall("after a while hello again".encode("utf-8"))
        
        client_list.remove(self)
        print("Connection lost with: ", addr)
        if len(client_list) == 0:
            kill.set()


def killer():
    while True:
        if kill.is_set():
            print("\nServer killed")
            os._exit(1)


HOST = config("HOST")
PORT = config("PORT", cast=int)

client_list = []
kill = threading.Event()

threading.Thread(target=killer).start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)

    print("Server is listening")

    while True:
        conn, addr = s.accept()

        client_thread = threading.Thread(target=Client, args=(conn, addr))
        client_thread.start()

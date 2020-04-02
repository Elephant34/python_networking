'''
The main server script which will recieve and handel requests
'''
import os
import socket
import threading

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
            self.send_msg("Server", "Connection Estabilished")

            full_msg = ''
            while True:
                try:
                    msg = self.conn.recv(2048)
                except ConnectionResetError:
                    break
                if not msg:
                    break
                full_msg += msg.decode("utf-8")
            
            if full_msg.lower() == "kill":
                kill.set()
            else:
                for client in client_list:
                    client.send_msg("Name", full_msg)
        
        client_list.remove(self)
        print("Connection lost with: ", addr)
    
    def send_msg(self, msg_from, message):
        '''
        Sends a message to this socket
        '''

        print("[{msg_from}] {message}".format(msg_from=msg_from, message=message))
        self.conn.sendall("[{msg_from}] {message}".format(msg_from=msg_from, message=message).encode("utf-8"))
        print("sent")
        return

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

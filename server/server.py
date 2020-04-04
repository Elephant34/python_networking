'''
A simple chat app server
To be run on a local network accessed via client
'''

import socket
import threading
from decouple import config
import os

class Client(threading.Thread):
    '''
    A thread created for every connected client
    '''

    def __init__(self, conn, addr):
        '''
        Sets the thread
        '''

        self.conn = conn
        self.addr = addr

        threading.Thread.__init__(self)
        self.start()
    
    def run(self):
        '''
        Sets up the main thread loop
        '''

        global client_list
        global messages
        global COMMANDS

        # Gets the client list and stops others using it
        client_list_lock.acquire()
        client_list.append(self)
        # Allows other threads to get the client list again
        client_list_lock.release()


        print("New connection at: ", self.addr)

        self.send_message("Please enter your name:", "Server")

        self.username = self.recieve_message()
        print(self.username)

        while True:
            msg = self.recieve_message()

            if msg[:2] == "//":
                # Test if the message is a server command
                command = msg[2:]
                if command not in COMMANDS:
                    self.send_message("Sorry that command wasn't recognised", "Server")
                    continue
                else:
                    if command == "kill":
                        # kill the server
                        kill_server()
                        continue
                    elif command == "quit":
                        break
                    elif command == "test":
                        self.send_message("You are connected to the server", "Server")
                        continue


            messages_lock.acquire()
            messages.append([msg, self.username])
            messages_lock.release()

        self.close()

    def recieve_message(self):
        '''
        Recieves a message from the client
        '''

        header = self.conn.recv(8).decode("utf-8")
        full_msg = self.conn.recv(int(header)).decode("utf-8")
        
        return full_msg
    
    def send_message(self, message, msg_from):
        '''
        sends a message to the client
        '''

        send_data = "[{msg_from}] {message}".format(msg_from=msg_from, message=message)
        send_data = format(len(send_data), "08d") + send_data
        self.conn.sendall(send_data.encode("utf-8"))

    def close(self):
        '''
        Closes the socket instances and ends the thread
        '''

        client_list_lock.acquire()
        client_list.remove(self)
        client_list_lock.release()

        self.conn.close()

        print("Connection closed at: ", self.addr)

def message_spool():
    '''
    Sends out any new messages to all connected clients
    '''
    global messages

    while True:

        if messages:
            messages_lock.acquire()
            client_list_lock.acquire()
            for msg, name in messages:
                for client in client_list:
                    client.send_message(msg, name)
            messages = []
            messages_lock.release()
            client_list_lock.release()

def kill_server():
    global client_list

    client_list_lock.acquire()
    local_copy = client_list
    client_list_lock.release()

    for client in local_copy:
        client.send_message("__die__", "Server")
        client.close()
    
    os._exit(1)

HOST = config("HOST")
PORT = config("PORT", cast=int)

COMMANDS = ("kill", "quit", "test")

# Shared varibales have a lock so two threads don't read at the same time
client_list_lock = threading.Lock()
client_list = []

messages_lock = threading.Lock()
messages = []

if __name__ == "__main__":

    print("Sever started...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)

        threading.Thread(target=message_spool).start()

        while True:
            conn, addr = s.accept()

            print("Serever listening...")

            # Creates a new client
            Client(conn, addr)
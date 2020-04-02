'''
A simple chat app server
To be run on a local network accessed via client
'''

import socket
import threading
from decouple import config

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
    
    def send_message(self, message):
        '''
        sends a message to the client
        '''



HOST = config("HOST")
PORT = config("PORT", cast=int)

condition = threading.Condition()
client_list = []
messages = []


'''
The main client script to send requests to the server
'''
import os
import socket
import threading
import tkinter as tk

from decouple import config


class App(threading.Thread):

    def __init__(self, s):
        self.s = s
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        message_ent = tk.Entry(self.root)
        message_ent.pack(side=tk.LEFT)

        send_btn = tk.Button(self.root, text="send", command=lambda: send(self.s, message_ent))
        send_btn.pack(side=tk.LEFT)

        self.root.mainloop()

HOST = config("HOST")
PORT = config("PORT", cast=int)

def send(s, message_ent):

    send_msg = message_ent.get()

    if send_msg == "exit":
        os._exit(1)
    else:
        s.sendall(send_msg.encode("utf-8"))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    app = App(s)

    s.connect((HOST, PORT))

    while True:
        full_msg = ''
        while True:
            print("Waiting...")
            msg = s.recv(2048)
            print(msg)
            if len(msg) == 0:
                break
            full_msg += msg.decode("utf-8")
        print(full_msg)
    

print("connection closed")

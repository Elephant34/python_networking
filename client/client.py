'''
A chat app client
To be run with the server on a local network
'''
import socket
import threading
from time import sleep
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from decouple import config


class ChatApp(threading.Thread):
    '''
    The main GUI of the chat app client
    '''

    def __init__(self):
        '''
        Sets the thread
        '''
        threading.Thread.__init__(self)
        self.start()
    
    def callback(self):
        self.root.quit()
    
    def run(self):
        '''
        Sets up the GUI when the thread starts
        '''

        self.root = tk.Tk()
        self.root.title("Chat Client")
        self.root.minsize(300, 400)
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        self.message_box = ScrolledText(self.root)
        self.message_box.grid(row=0, column=0, stick="nsew", padx=2.5, pady=2.5, columnspan=2)

        self.add_text("Message system is loading...")

        self.message = tk.StringVar()
        message_ent = tk.Entry(self.root, textvariable=self.message)
        message_ent.grid(row=1, column=0, stick="nsew", padx=2.5, pady=2.5)

        message_ent.focus()

        send_btn = tk.Button(self.root, command=lambda: self.send(), text="send")
        send_btn.grid(row=1, column=1, stick="nsew", padx=2.5, pady=2.5)
        
        self.root.rowconfigure(0, weight=25)
        self.root.rowconfigure(1, weight=1)

        self.root.columnconfigure(0, weight=5)
        self.root.columnconfigure(1, weight=1)

        message_ent.bind("<Return>", lambda e: self.send())

        self.root.mainloop()
    
    def add_text(self, text):
        '''
        Adds text to the end of the message bored
        '''
        self.message_box.config(state="normal")
        self.message_box.insert(tk.END, text + "\n")
        self.message_box.see(tk.END)
        self.message_box.config(state="disabled")

    def send(self):
        '''
        Sends the message to the server
        '''

        send = self.message.get().encode("utf-8")
        self.message.set("")

def recieve_message(s):
    full_msg = ""
    while True:
        msg = s.recv(2048)
        if not msg:
            break
        full_msg += msg.decode("utf-8")


HOST = config("HOST")
PORT = config("PORT", cast=int)


if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        app = ChatApp()

        connected = False

        try:
            s.connect((HOST, PORT))
            connected=True
        except ConnectionRefusedError:
            app.add_text("Couldn't connect to server")
            app.add_text("Are you sure it is running?")

        if connected:
            app.add_text("Successfully connected to server.")
            app.add_text("Type 'quit' anytime to exit\n")


            while True:
                message = recieve_message(s)

                if message == "__die__":
                    break
            
                app.add_text(full_msg)

    app.add_text("\nQuitting")
    sleep(3)
    app.root.quit()
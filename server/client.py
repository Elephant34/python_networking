'''
A chat app client
To be run with the server on local network
'''
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

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
    
    def run(self):
        '''
        Sets up the GUI when the thread starts
        '''

        self.root = tk.Tk()
        self.root.title("Chat Client")
        self.root.minsize(300, 400)

        ''' OLD CODE- message widgets can't support scrollbars... :(
        self.text = tk.StringVar()
        self.text.set("Message system is loading...")

        message_box = tk.Message(self.root, textvariable=self.text, width=290, anchor=tk.NW)
        message_box.grid(row=0, column=0, stick="nsew", padx=2.5, pady=2.5, columnspan=2)
        '''
        self.message_box = ScrolledText(self.root)
        self.message_box.grid(row=0, column=0, stick="nsew", padx=2.5, pady=2.5, columnspan=2)

        self.set_text("Message system is loading...")

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
    
    def set_text(self, text):
        '''
        Adds text to the end of the message bored
        '''
        self.message_box.config(state="normal")
        self.message_box.insert(tk.END, text)
        self.message_box.see(tk.END)
        self.message_box.config(state="disabled")

    def send(self):
        '''
        Sends the message to the server
        '''

        send = self.message.get().encode("utf-8")
        self.message.set("")

        self.set_text("\n"+send.decode("utf-8"))
        print(send.decode("utf-8"))


if __name__ == "__main__":

    app = ChatApp()
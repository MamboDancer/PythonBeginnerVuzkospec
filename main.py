import random

import zerorpc
from threading import Thread
from tkinter import *


class Game:
    root = Tk()
    start_widgets = []
    room_id = None
    client = zerorpc.Client()
    value = 10

    def __init__(self):
        Button(self.root, text="set", command=self.client.rpc_set_value).pack()
        Button(self.root, text="get", command=self.client.rpc_get_value).pack()
        self.root.geometry("400x400")
        self.root.title("Game")
        self.root.resizable(False, False)
        self.init_start_window()

    def init_start_window(self):
        self.start_entry = Entry(self.root)
        create_room_button = Button(self.root, text="Create Room", command=self.create_room)
        connect_to_room_button = Button(self.root, text="Connect to room", command=self.connect_to_room)
        self.start_widgets.append(self.start_entry)
        self.start_widgets.append(create_room_button)
        self.start_widgets.append(connect_to_room_button)
        for widget in self.start_widgets:
            widget.pack()

    def create_room(self):
        self.room_id = int(self.start_entry.get())
        zerorpc_thread = Thread(target=self.start_server_room)
        zerorpc_thread.daemon = True
        zerorpc_thread.start()
        self.connect_to_room()

    def connect_to_room(self):
        self.room_id = int(self.start_entry.get())
        self.client.connect(f"tcp://127.0.0.1:{self.room_id}")
        self.show_toplevel("Connected", f"Connected to room {self.room_id}")
        self.unload_start_widgets()

    def unload_start_widgets(self):
        for widget in self.start_widgets:
            widget.destroy()

    def start_server_room(self):
        try:
            s = zerorpc.Server(self)
            s.bind(f"tcp://0.0.0.0:{self.room_id}")
            print("Server running")
            self.unload_start_widgets()
            s.run()
        except:
            self.show_toplevel("Error", f"Could not start server on port {self.room_id}")

    def show_toplevel(self, title, text):
        message = Toplevel(self.root)
        message.title(title)
        message.resizable(False, False)
        Label(message, text=text).pack()
        Button(message, text="Close", command=message.destroy).pack()

    def rpc_set_value(self):
        self.value = random.randint(25, 125)

    def rpc_get_value(self):
        print(self.value)

    def rpc_send_message(self, message):
        pass

    def run(self):
        self.root.mainloop()


Game().run()

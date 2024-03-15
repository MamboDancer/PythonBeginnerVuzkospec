from client import GameClient
from server import GameServer
from tkinter import *
import socket


class Game:
    root = Tk()
    game_widgets = []
    ip = None
    port = None
    server = GameServer()
    user_client = GameClient(root)

    def __init__(self):
        self.root.geometry("440x480")
        self.root.title("Tic-Tac-Toe Online")
        self.root.resizable(False, False)
        hostname = socket.gethostname()
        self.client_ip = socket.gethostbyname(hostname)
        self.init_start_window()
        self.init_game()

    def init_start_window(self):
        self.entry_toplevel = Toplevel(self.root)
        self.ip_entry = Entry(self.entry_toplevel)
        self.port_entry = Entry(self.entry_toplevel)
        self.name_entry = Entry(self.entry_toplevel)
        Label(self.entry_toplevel, text=f"Your IP-address: {self.client_ip}").pack()
        self.ip_entry.pack()
        self.port_entry.pack()
        self.name_entry.pack()
        Button(self.entry_toplevel, text="Create Room", command=self.create_room).pack()
        Button(self.entry_toplevel, text="Connect to room", command=self.connect_to_room).pack()
        self.ip_entry.insert(0, self.client_ip)
        self.name_entry.insert(0, "Username")

    def init_game(self):
        i = 0
        for x in range(3):
            for y in range(3):
                self.game_widgets.append(Button(self.root,
                                                width=6,
                                                height=3,
                                                font=("Arial", 30),
                                                command=lambda a=i: self.user_client.make_move(a)))
                self.game_widgets[i].grid(row=x, column=y)
                i += 1

    def create_room(self):
        self.ip = self.ip_entry.get()
        self.port = self.port_entry.get()
        self.start_server_room()
        self.connect_to_room()

    def connect_to_room(self):
        self.ip = self.ip_entry.get()
        self.port = self.port_entry.get()
        self.user_client.connect(self.ip, self.port)
        self.show_toplevel("Connected", f"Connected to room {self.port}")
        self.user_client.player_name = self.name_entry.get()
        self.entry_toplevel.destroy()
        self.user_client.game_buttons = self.game_widgets
        self.user_client.refresh_board()

    def start_server_room(self):
        try:
            self.user_client.start_server_room(self.ip, self.port, self.server)
        except:
            self.show_toplevel("Error", f"Could not start server on port {self.port}")

    def show_toplevel(self, title, text):
        message = Toplevel(self.root)
        message.title(title)
        message.resizable(False, False)
        Label(message, text=text).pack()
        Button(message, text="Close", command=message.destroy).pack()

    def run(self):
        self.root.mainloop()


tictactoe = Game()
tictactoe.run()


import time
import gevent
import zerorpc
from tkinter import *


class Server:
    game_board = [-1] * 9
    active_player = True

    def rpc_get_board(self):
        return self.game_board

    def rpc_make_move(self, move_index, player):
        if player == self.active_player and self.game_board[move_index] == -1:
            self.game_board[move_index] = int(self.active_player)
            if self.active_player:
                self.active_player = False
            else:
                self.active_player = True
            return 1
        else:
            return 0


class Client:
    client = zerorpc.Client(timeout=2)
    is_host = False
    game_window = None
    board = []
    is_moved = False

    def __init__(self, root):
        self.game_window = root

    def connect(self, room_id):
        self.client.connect(f"tcp://127.0.0.1:{room_id}")

    def start_server_room(self, room_id, server):
        s = zerorpc.Server(server)
        s.bind(f"tcp://0.0.0.0:{room_id}")
        print("Server running")
        self.is_host = True
        gevent.spawn(s.run)

    def make_move(self, value):
        self.client.rpc_make_move(value, self.is_host)
        if not self.is_moved:
            self.refresh_board()
            self.is_moved = True

    def refresh_board(self):
        self.board = self.client.rpc_get_board()
        self.set_points()
        self.game_window.after(100, self.refresh_board)

    def set_points(self):
        buttons = self.game_window.winfo_children()
        for i in range(len(self.board)):
            mark = " "
            if self.board[i] == 0:
                mark = "O"
            if self.board[i] == 1:
                mark = "X"
            buttons[i].config(text=mark)


class Game:
    root = Tk()
    start_widgets = []
    game_widgets = []
    room_id = None
    server = Server()
    client = Client(root)

    def __init__(self):
        self.root.geometry("440x480")
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

    def init_game(self):
        i = 0
        for x in range(3):
            for y in range(3):
                self.game_widgets.append(Button(self.root,
                                                width=6,
                                                height=3,
                                                font=("Arial", 30),
                                                command=lambda a=i: self.client.make_move(a)))
                self.game_widgets[i].grid(row=x, column=y)
                i += 1

    def create_room(self):
        self.room_id = int(self.start_entry.get())
        self.start_server_room()
        self.connect_to_room()

    def connect_to_room(self):
        self.room_id = int(self.start_entry.get())
        self.client.connect(self.room_id)
        self.show_toplevel("Connected", f"Connected to room {self.room_id}")
        self.unload_start_widgets()
        self.init_game()

    def unload_start_widgets(self):
        for widget in self.start_widgets:
            widget.destroy()

    def start_server_room(self):
        try:
            self.client.start_server_room(self.room_id, self.server)
        except:
            self.show_toplevel("Error", f"Could not start server on port {self.room_id}")

    def show_toplevel(self, title, text):
        message = Toplevel(self.root)
        message.title(title)
        message.resizable(False, False)
        Label(message, text=text).pack()
        Button(message, text="Close", command=message.destroy).pack()

    def run(self):
        self.root.mainloop()


Game().run()
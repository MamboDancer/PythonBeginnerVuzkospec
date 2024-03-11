import gevent
import zerorpc


class Client:
    client = zerorpc.Client(timeout=2)
    is_host = False
    game_window = None
    game_buttons = None
    board = []

    def __init__(self, root):
        self.game_window = root

    def connect(self, ip, room_id):
        self.client.connect(f"tcp://{ip}:{room_id}")

    def start_server_room(self, ip, room_id, server):
        s = zerorpc.Server(server)
        s.bind(f"tcp://{ip}:{room_id}")
        self.is_host = True
        gevent.spawn(s.run)

    def make_move(self, value):
        self.client.rpc_make_move(value, self.is_host)

    def refresh_board(self):
        self.board = self.client.rpc_get_board()
        self.set_points()
        self.game_window.after(100, self.refresh_board)

    def set_points(self):
        for i in range(len(self.board)):
            mark = " "
            if self.board[i] == 0:
                mark = "O"
            if self.board[i] == 1:
                mark = "X"
            self.game_buttons[i].config(text=mark)

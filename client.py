import gevent
import zerorpc
from tkinter import *
from leaderboard import Leaderboard

lb_url = "http://dreamlo.com/lb/VbnIEzmDzUCLZuACa_jCqQ2faOJKPJB0OvdOafEBYqSA"
lb = Leaderboard(lb_url)


class GameClient:
    client = zerorpc.Client(timeout=2)
    is_host = False
    game_window = None
    game_buttons = None
    board = []
    player_name = None

    def __init__(self, root):
        self.game_window = root

    def connect(self, ip, room_id):
        self.client.connect(f"tcp://{ip}:{room_id}")
        self.show_leaderboard()

    def start_server_room(self, ip, room_id, server):
        s = zerorpc.Server(server)
        s.bind(f"tcp://{ip}:{room_id}")
        self.is_host = True
        gevent.spawn(s.run)

    def make_move(self, value):
        move = self.client.rpc_make_move(value, self.is_host)
        if not move:
            t = Toplevel(self.game_window)
            Label(t, text=f"It is not your turn!").pack()
        if move == -1:
            t = Toplevel(self.game_window)
            Label(t, text=f"Space occupied!").pack()

    def refresh_board(self):
        self.board, winner = self.client.rpc_get_board()
        gevent.sleep(0.025)
        self.set_points()
        active_player = self.client.rpc_get_active_player()
        if active_player == self.is_host:
            self.game_window.title("Your turn")
        else:
            self.game_window.title("Enemy turn")
        if winner >= 0:
            t = Toplevel(self.game_window)
            Label(t, text=f"Winner is {'X' if winner else 'O'}").pack()
            if winner == self.is_host:
                lb.update_leaderboard(self.player_name)
            return 0
        if winner == -2:
            t = Toplevel(self.game_window)
            Label(t, text=f"DRAW").pack()
            return 0
        self.game_window.after(50, self.refresh_board)

    def set_points(self):
        marks = {
            0: "O",
            1: "X",
            -1: " "
        }
        for i in range(len(self.board)):
            mark = marks.get(self.board[i])
            self.game_buttons[i].config(text=mark)

    def show_leaderboard(self):
        score_toplevel = Toplevel(self.game_window)
        score_toplevel.title("Wins Leaderboard")
        for score in lb.get_scores():
            Label(score_toplevel, text=f"Name: {score['name']}, Wins: {score['score']}").pack()
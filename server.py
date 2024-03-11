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

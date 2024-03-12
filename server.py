class GameServer:
    game_board = [-1] * 9
    active_player = True

    def rpc_get_board(self):
        return self.game_board, self.check_winner()

    def rpc_make_move(self, move_index, player): #
        if player == self.active_player and self.game_board[move_index] == -1:
            self.game_board[move_index] = int(self.active_player)
            if self.active_player:
                self.active_player = False
            else:
                self.active_player = True
        return -1

    def check_winner(self):
        for i in range(3):
            if self.game_board[i] == self.game_board[i + 3] == self.game_board[i + 6] != -1:
                return self.game_board[i]
        for i in range(0, 9, 3):
            if self.game_board[i] == self.game_board[i + 1] == self.game_board[i + 2] != -1:
                return self.game_board[i]
        if self.game_board[0] == self.game_board[4] == self.game_board[8] != -1:
            return self.game_board[0]
        if self.game_board[2] == self.game_board[4] == self.game_board[6] != -1:
            return self.game_board[2]
        return -1

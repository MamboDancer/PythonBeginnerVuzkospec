class GameServer:
    game_board = [-1] * 9
    active_player = True

    def rpc_get_board(self):
        winner = self.check_winner()
        return self.game_board, winner

    def rpc_get_active_player(self):
        return self.active_player

    def rpc_make_move(self, move_index, player):
        if player == self.active_player:
            if self.game_board[move_index] == -1:
                self.game_board[move_index] = int(self.active_player)
                self.active_player = not self.active_player
                return 1
            else:
                return -1
        return 0

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

        count = 0
        for i in range(len(self.game_board)):
            if self.game_board[i] != -1:
                count += 1
        if count == 9:
            return -2
        return -1

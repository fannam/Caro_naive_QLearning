from const import *
class GameState:
    def __init__(self):
        self.board = [['--' for _ in range(COLS)] for _ in range(ROWS)]
        self.players = ['X', 'O']
        self.current_player =  self.players[0]
        self.game_over = False
        self.winner = None

    def isValidMove(self, row, col):
        return self.board[row][col]=='--'
    
    def isGameOver(self):
        return self.checkInARow(WINNING_COUNT, self.players[0]) or self.checkInARow(WINNING_COUNT, self.players[1])

    def isBoardFull(self):
        for row in self.board:
            for piece in row:
                if piece == '--':
                    return False
        return True

    def checkInARow(self, N, player):
        for row in self.board:
            count = 0
            for piece in row:
                if piece == player:
                    count += 1
                    if count == N:
                        self.game_over = True
                        self.winner = player
                        return True
                else:
                    count = 0
        #check col
        for col in range(COLS):
            count = 0
            for row in range(ROWS):
                if self.board[row][col] == player:
                    count += 1
                    if count == N:
                        self.game_over = True
                        self.winner = player
                        return True
                else:
                    count = 0
        #check diagonal (top-left to bot-right)
        for row in range(ROWS - N + 1):
            for col in range(COLS - N + 1):
                count = 0
                for i in range(N):
                    if self.board[row + i][col + i] == player:
                        count += 1
                        if count == N:
                            self.game_over = True
                            self.winner = player
                            return True
                    else:
                        count = 0

        #check diagonal (top-right to bot-left)
        for row in range(N - 1, ROWS):
            for col in range(COLS - N + 1):
                count = 0
                for i in range(N):
                    if self.board[row - i][col + i] == player:
                        count += 1
                        if count == N:
                            self.game_over = True
                            self.winner = player
                            return True
                    else:
                        count = 0
    
    def switch_player(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]
    
    def avaiable_moves(self):#action set
        moves = []
        for i in range (ROWS):
            for j in range (COLS):
                if self.board[i][j] == '--':
                    moves.append((i, j))
        return moves
    
    def make_move(self, move):#action
        row, col = move

        if self.isValidMove(row, col):
            self.board[row][col] = self.current_player

            if self.checkInARow(WINNING_COUNT, self.current_player):
                self.game_over = True
                self.winner = self.current_player
            elif self.isBoardFull():
                self.game_over = True

            self.switch_player()
        else:
            print("Invalid move. Try again.")
    
    def get_state(self):
        return self
    






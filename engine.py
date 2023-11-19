from const import *
class GameState:
    def __init__(self):
        self.board = [['--' for _ in range(COLS)] for _ in range(ROWS)]

    def _isValidMove(self, row, col):
        return self.board[row][col]=='--'
    
    def _isGameOver(self):
        return self._checkInARow(WINNING_COUNT, 'X') or self._checkInARow(WINNING_COUNT, 'O')

    def _isBoardFull(self):
        for row in self.board:
            for piece in row:
                if piece == '--':
                    return False
        return True

    def _checkInARow(self, N, player):
        #check row
        for row in self.board:
            count = 0
            for piece in row:
                if piece == player:
                    count += 1
                    if count == N:
                        print(player + " is win")
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
                        print(player + " is win")
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
                            print(player + " is win")
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
                            print(player + " is win")
                            return True
                    else:
                        count = 0

from const import *
class GameState:
    def __init__(self):
        self.board = [['--' for _ in range(COLS)] for _ in range(ROWS)]

    def _isValidMove(self, row, col):
        return self.board[row][col]=='--'
    
    def _isGameOver(self):
        pass

    def _checkInARow(self, N, player):
        pass
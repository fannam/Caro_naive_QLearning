from const import *
class GameState:
    def __init__(self):
        self.board = [['--' for _ in range(COLS)] for _ in range(ROWS)]
        self.players = ['X', 'O']
        self.current_player =  self.players[0]
        self.game_over = False
        self.winner = None
        self.trace_move = []

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
    
    def available_moves(self):#action set
        moves = []
        for i in range (ROWS):
            for j in range (COLS):
                if self.board[i][j] == '--':
                    moves.append((i, j))
        return moves
    
    def make_move(self, move, player):#action
        row, col = move
        self.last_move = move
        if self.isValidMove(row, col):
            self.board[row][col] = player

            if self.checkInARow(WINNING_COUNT, player):
                self.game_over = True
                self.winner = player
            elif self.isBoardFull():
                self.game_over = True

            self.switch_player()
        else:
            print("Invalid move. Try again.")      

    def undo_move(self, move):
        row, col = move
        self.board[row][col] = '--'
        self.switch_player()
    
    ####
    # ... (other methods in GameState)

    def evaluate_move_quality_in_attack(self, move, player):
        init_row, init_col = move
        count = 0

        row = init_row
        while row + 1 < ROWS and (self.board[row+1][init_col] == player):
            count += 1
            row += 1

        row = init_row
        while row > 0 and (self.board[row-1][init_col] == player):
            count += 1
            row -= 1

        col = init_col
        while col + 1 < COLS and (self.board[init_row][col+1] == player):
            count += 1
            col += 1

        col = init_col
        while col > 0 and (self.board[init_row][col-1] == player):
            count += 1
            col -= 1
        if player == 'X':
            return count*1.5
        else:
            return count*(-1)*1.5

    def evaluate_move_quality_in_defense(self, move, opponent):
        init_row, init_col = move
        count = 0

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

        for direction in directions:
            row, col = init_row, init_col
            length = 0

            while (0 <= row < ROWS) and (0 <= col < COLS) and (self.board[row][col] == opponent):
                length += 1
                row += direction[0]
                col += direction[1]

            count += length

        if opponent == 'X':
            return count*(-1)
        else:
            return count
        
    def evaluate_game_state_with_new_move(self, player, N):
        total = 0
        for row in self.board:
            count = 0
            for piece in row:
                if piece == player:
                    count += 1
                else:
                    total += count
                    count = 0
        #check col
        for col in range(COLS):
            count = 0
            for row in range(ROWS):
                if self.board[row][col] == player:
                    count += 1                      
                else:
                    total += count
                    count = 0
        #check diagonal (top-left to bot-right)
        for row in range(ROWS - N + 1):
            for col in range(COLS - N + 1):
                count = 0
                for i in range(N):
                    if self.board[row + i][col + i] == player:
                        count += 1
                    else:
                        total += count
                        count = 0

        #check diagonal (top-right to bot-left)
        for row in range(N - 1, ROWS):
            for col in range(COLS - N + 1):
                count = 0
                for i in range(N):
                    if self.board[row - i][col + i] == player:
                        count += 1
                    else:
                        total += count
                        count = 0
        return total
        # if player == 'X':
        #     return total 
        # elif player == 'O':
        #     return total * (-1)
    
    





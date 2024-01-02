from const import *
import copy
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
        self.game_over = True
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
        #self.last_move = move
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
          
    def evaluate_game_state_with_new_move_ver2(self, player, N):
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
        if total <= 2:
            return -5
        else:
            return total

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
        if player == 'X':
            return total 
        elif player == 'O':
            return total * (-1)
    

    def minimax(self, depth, alpha, beta, maximizing_player):
        temp_state = copy.deepcopy(self)
        if depth == 0 or self.game_over:
            return evaluate_state(temp_state)

        if maximizing_player:
            max_eval = float('-inf')
            for move in temp_state.available_moves():
                temp_state.make_move(move, temp_state.current_player)
                eval = temp_state.minimax(depth - 1, alpha, beta, False)
                temp_state.undo_move(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for move in temp_state.available_moves():
                temp_state.make_move(move, temp_state.current_player)
                eval = temp_state.minimax(depth - 1, alpha, beta, True)
                temp_state.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

        
    def get_best_move(self):
        best_move = None
        best_eval = float('-inf') if self.current_player == 'X' else float('inf')

        for move in self.available_moves():
            self.make_move(move, self.current_player)
            eval = self.minimax(3, float('inf'), float('-inf'), False)  # Adjust the depth as needed
            self.undo_move(move)

            if (self.current_player == 'X' and eval > best_eval) or (self.current_player == 'O' and eval < best_eval):
                best_eval = eval
                best_move = move

        return best_move

    def count_open_paths(self, player, N):
        open_paths = 0
        rows, cols = len(self.board), len(self.board[0])

        def check_line(line):
            nonlocal open_paths
            count = 0
            for cell in line:
                if cell == player or cell == '--':
                    count += 1
                    if count == N:
                        open_paths += 1
                else:
                    count = 0

        # Check rows and columns
        for i in range(rows):
            check_line(self.board[i])
            check_line([self.board[j][i] for j in range(cols)])

        # Check diagonals
        for i in range(rows - N + 1):
            for j in range(cols - N + 1):
                check_line([self.board[i + k][j + k] for k in range(N)])
                check_line([self.board[i + k][j + N - 1 - k] for k in range(N)])
        #print(open_paths)
        return open_paths

def evaluate_state(state):
    opponent = 'O' if state.current_player == 'X' else 'X'
    player_open_paths = state.count_open_paths(state.current_player, WINNING_COUNT)
    opponent_open_paths = state.count_open_paths(opponent, WINNING_COUNT)

        # Gán điểm tùy thuộc vào số đường mở của người chơi và đối thủ
    score = player_open_paths - opponent_open_paths
    return score




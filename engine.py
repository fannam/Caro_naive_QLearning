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
        return 0<=row and row<ROWS and 0<=col and col<COLS and self.board[row][col]=='--'
    
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
    
    def valid_neighbour_moves(self):
        all_moves = []
        can_use_moves = []

        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] != '--':
                    # Get neighbors for the current piece
                    neighbors = get_neighbours((i, j))

                    # Accumulate all neighbors
                    all_moves.extend(neighbors)
                else:
                    # Count the number of valid moves
                    can_use_moves.append((i, j))

    # If all cells are empty, return the center cell
        if not all_moves:
            return [((ROWS - 1) // 2, (COLS - 1) // 2)]

    # Filter out duplicates and invalid moves
        can_use_moves = list(set(can_use_moves) & set(all_moves))
        
        return can_use_moves
    
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
            for move in temp_state.valid_neighbour_moves():
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
            for move in temp_state.valid_neighbour_moves():
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
        best_move = check_winning_move(self)
        if best_move == None:
            best_move = check_has_to_block(self)
            if best_move == None:
                best_move = check_make_four_in_a_row(self)
                if best_move == None:
                    best_move = check_block_three_in_a_row(self)
                    if best_move == None:
                        best_eval = float('-inf') if self.current_player == 'X' else float('inf')

                        for move in self.valid_neighbour_moves():
                            self.make_move(move, self.current_player)
                            eval = self.minimax(5, float('inf'), float('-inf'), False)  # Adjust the depth as needed
                            self.undo_move(move)

                            if (self.current_player == 'X' and eval > best_eval) or (self.current_player == 'O' and eval < best_eval):
                                best_eval = eval
                                best_move = move
                    else:
                        return best_move
                else:
                    return best_move

                #return best_move
            else:
                return best_move
        else:
            return best_move
    def count_open_paths_v2(self, player, N):
        open_paths = 0
        rows, cols = len(self.board), len(self.board[0])

        def check_direction(start, direction):
            nonlocal open_paths
            count = 0
            has_player_piece = False
            i, j = start

            for _ in range(N):
                if 0 <= i < rows and 0 <= j < cols:
                    cell = self.board[i][j]
                    if cell == player:
                        has_player_piece = True
                        count += 1
                        if count == N:
                            open_paths += 1
                            break
                    elif cell == '--':
                        count += 1
                    else:
                        break
                    i, j = i + direction[0], j + direction[1]
                else:
                    break

            if not has_player_piece:
                open_paths -= count // N

        # Check all directions
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Right, Down, Diagonal right-down, Diagonal left-down

        for i in range(rows):
            for j in range(cols):
                for direction in directions:
                    check_direction((i, j), direction)

        return open_paths
    
    def count_open_paths(self, player, N):
        open_paths = 0
        rows, cols = len(self.board), len(self.board[0])

        def check_line(line):
            nonlocal open_paths
            count = 0
            has_player_piece = False
            
            for cell in line:
                if cell == player:
                    has_player_piece = True
                    count += 1
                    if count == N:
                        open_paths += 1
                elif cell == '--':
                    count += 1
                    if count == N:
                        open_paths += 1
                else:
                    count = 0
                    has_player_piece = False

            if not has_player_piece:
                open_paths -= count // N

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
    player_open_paths = state.count_open_paths_v2(state.current_player, WINNING_COUNT)
    opponent_open_paths = state.count_open_paths_v2(opponent, WINNING_COUNT)
    score = player_open_paths - opponent_open_paths
    return score

def check_winning_move(state):
    temp_state = copy.deepcopy(state)
    available_moves = state.available_moves()
    player = state.current_player
    for move in available_moves:
        temp_state.make_move(move, player)
        #print(temp_state.board)
        if temp_state.checkInARow(WINNING_COUNT, player):
            return move
        temp_state.undo_move(move)

    return None

def check_has_to_block(state):
    temp_state = copy.deepcopy(state)
    available_moves = state.available_moves()
    next_player = 'X' if temp_state.current_player == 'O' else 'O'
    for move in available_moves:
        
        temp_state.make_move(move, next_player)

        if temp_state.checkInARow(WINNING_COUNT, next_player):
            return move

        temp_state.undo_move(move)

    return None

def check_make_four_in_a_row(state):
    temp_state = copy.deepcopy(state)
    available_moves = state.valid_neighbour_moves()
    player = state.current_player
    for move in available_moves:
        temp_state.make_move(move, player)
        if temp_state.checkInARow(4, player):
            # Check if making four in a row can lead to five in a row
            next_avaiable_moves = temp_state.valid_neighbour_moves()
            for next_move in next_avaiable_moves:
                temp_state.make_move(move, player)
                if temp_state.checkInARow(5, player):
                    return move
        temp_state.undo_move(move)
    return None

# def check_block_three_in_a_row(state):
#     temp_state = copy.deepcopy(state)
#     available_moves = state.valid_neighbour_moves()
#     next_player = 'X' if temp_state.current_player == 'O' else 'O'
#     for move in available_moves:
#         temp_state.make_move(move, next_player)
#         if temp_state.checkInARow(3, next_player):
#             # Check if blocking three in a row can lead to five in a row
#             if check_potential_five_in_a_row(temp_state, next_player):
#                 return move
#         temp_state.undo_move(move)
#     return None
def check_block_three_in_a_row(state):
    temp_state = copy.deepcopy(state)
    available_moves = temp_state.valid_neighbour_moves()
    next_player = 'X' if state.current_player == 'O' else 'O'

    for move in available_moves:
        temp_state.make_move(move, next_player)
        if temp_state.checkInARow(4, next_player):
            print(temp_state.board)
            next_avaiable_moves = temp_state.valid_neighbour_moves()
            for next_move in next_avaiable_moves:
                temp_state.make_move(next_move, next_player)
                if temp_state.checkInARow(5, next_player):
                    return move
                temp_state.undo_move(next_move)
        temp_state.undo_move(move)
    return None

# Add this method in the GameState class
def check_potential_five_in_a_row(state, player):
    for move in state.valid_neighbour_moves():
        state.make_move(move, player)
        if state.checkInARow(5, player):
            state.undo_move(move)
            return True
        state.undo_move(move)
    return False

def check_open_ends(state, row, col):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for direction in directions:
        if state.isValidMove(row + direction[0], col + direction[1] - 1) and \
           state.isValidMove(row + direction[0], col + direction[1] + 3) and \
           state.board[row + direction[0]][col + direction[1] - 1] == '--' and \
           state.board[row + direction[0]][col + direction[1] + 3] == '--':
            return True

    return False

def get_neighbours(t):
    (i, j) = t
    neighbour_moves = [
        (i, j - 1),  # Left
        (i, j + 1),  # Right
        (i - 1, j),  # Top
        (i + 1, j),  # Bottom
        (i - 1, j - 1),  # Top-left
        (i - 1, j + 1),  # Top-right
        (i + 1, j - 1),  # Bottom-left
        (i + 1, j + 1),  # Bottom-right
    ]
    return neighbour_moves
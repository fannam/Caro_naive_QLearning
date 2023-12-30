from engine import GameState
from const import *
import numpy as np

class QLearningAgent:
    def __init__(self, alpha, epsilon, discount_factor):
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.reward = 0
        self.Q = {}
    
    def state_to_string(self, state):
        return str(state.board)

    def get_Q_value(self, state, action):
        state_str = self.state_to_string(state)
        return self.Q.get((state_str, action), np.random.uniform(-0.1, 0.1))#)
    
    def choose_action(self, state, available_moves):
        if np.random.rand() < self.epsilon:
            index = np.random.choice(len(available_moves))
            return available_moves[index]
        else:
            Q_value = [self.get_Q_value(state, move) for move in available_moves]
            if state.current_player == 'X':
                index = np.argmax(Q_value)
            elif state.current_player == 'O':
                index = np.argmin(Q_value)
            return available_moves[index]
    
    def update_Q_value(self, state, action, reward, next_state):
        state_str = self.state_to_string(state)
        if next_state.current_player == 'X':
            best_next_Q = np.max([self.get_Q_value(next_state, move) for move in next_state.available_moves()])
        elif next_state.current_player == 'O':
            best_next_Q = np.min([self.get_Q_value(next_state, move) for move in next_state.available_moves()])
        current_Q_value = self.get_Q_value(state, action)
        new_Q_value = (1 - self.alpha) * current_Q_value + self.alpha * (reward + self.discount_factor * best_next_Q)
        self.Q[(state_str, action)] = new_Q_value

    def train(self, num_episodes):
        
        for episode in range(num_episodes):
            state = GameState() 
            self.reward = 0.0  
            #print(state.board)         
            while not state.game_over:
                available_moves = state.available_moves()
                if len(available_moves)==0:
                    break
                action = self.choose_action(state, available_moves)
                current_state = state
                state.make_move(action, current_state.current_player)
                next_state = state
                next_avaiable_moves = next_state.available_moves()
                if next_state.isGameOver():
                    if next_state.winner == 'X':
                        self.reward = 100.0
                    elif next_state.winner == 'O':
                        self.reward = -100.0
                elif next_state.isBoardFull():
                    self.reward = 0.0
                else:
                    if current_state.current_player == 'X':
                        self.reward = next_state.evaluate_game_state_with_new_move('X', WINNING_COUNT)
                    else:
                        self.reward = next_state.evaluate_game_state_with_new_move('O', WINNING_COUNT)
                    
                if next_avaiable_moves:
                    self.update_Q_value(current_state, action, self.reward, next_state)
                
            print(f"Episode {episode + 1}/{num_episodes}, Winner: {state.winner}, Q-value updates: {len(self.Q)}")    
    def best_move(self, state):
        available_moves = state.available_moves()
        if len(available_moves) == 0:
            return None  # No available moves

        Q_values = [self.get_Q_value(state, move) for move in available_moves]
        if state.current_player == 'X':
            best_move_index = np.argmax(Q_values)
        elif state.current_player == 'O':
            best_move_index = np.argmin(Q_values)
        print(f"{state} {available_moves[best_move_index]} {self.get_Q_value(state, available_moves[best_move_index])}")
        return available_moves[best_move_index]
    
    def play(self):
        counter = 0
        while(counter<=1):
            state = GameState()
            while not state.isGameOver() and not state.isBoardFull():
                best_action = self.best_move(state)
                if best_action is None:
                    break
                state.make_move(best_action)
                for row in state.board:
                    print(row)
                print("--------")
            print(f"Game Over. Winner: {state.winner}")
            counter+=1
    def print_Q_value(self):
        for key, value in self.Q.items():
            print(f"Key: {key}, Value: {value}")
    #######

# agent = QLearningAgent(0.1, 0.3, 0.9)
# agent.train(1)
# agent.print_Q_value()



                      
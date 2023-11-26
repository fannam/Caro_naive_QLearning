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
    
    # def state_to_string(self, state):
    #     return str(state.board)

    def get_Q_value(self, state, action):
        #state_str = self.state_to_string(state)
        return self.Q.get((state, action), 0.0)#)
    
    def choose_action(self, state, available_moves):
        if np.random.rand() < self.epsilon:
            index = np.random.choice(len(available_moves))
            return available_moves[index]
        else:
            Q_value = [self.get_Q_value(state, move) for move in available_moves]
            index = np.argmax(Q_value)
            return available_moves[index]
    
    def update_Q_value(self, state, action, reward, next_state):
        #state_str = self.state_to_string(state)
        best_next_Q = np.max([self.get_Q_value(next_state, move) for move in next_state.available_moves()])
        # for move in next_state.available_moves():
        #     print(move)
        current_Q_value = self.get_Q_value(state, action)
        new_Q_value = (1 - self.alpha) * current_Q_value + self.alpha * (reward + self.discount_factor * best_next_Q)
        #print(new_Q_value)
        self.Q[(state, action)] = new_Q_value

    def train(self, num_episodes):
        for episode in range(num_episodes):
            state = GameState()            
            while not state.isGameOver() and not state.isBoardFull():
                available_moves = state.available_moves()
                if len(available_moves)==0:
                    break
                action = self.choose_action(state, available_moves)
                state.make_move(action)
                next_state = state
                next_avaiable_moves = next_state.available_moves()
                if next_avaiable_moves:
                    self.update_Q_value(state, action, self.reward, next_state)
            if state.winner == 'X':
                self.reward = 1.0
            elif state.isBoardFull():
                self.reward = 0.0
            else:
                self.reward = -10.0
            # for row in state.board:
            #     print(row) 
            print(f"Episode {episode + 1}/{num_episodes}, Winner: {state.winner}, Q-value updates: {len(self.Q)}")    
    def best_move(self, state):
        available_moves = state.available_moves()
        if len(available_moves) == 0:
            return None  # No available moves

        Q_values = [self.get_Q_value(state, move) for move in available_moves]
        best_move_index = np.argmax(Q_values)
        #print(f"{state} {available_moves[best_move_index]} {self.get_Q_value(state, available_moves[best_move_index])}")
        return available_moves[best_move_index]
    
    def play(self):
        counter = 0
        while(counter<10):
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

agent = QLearningAgent(0.1, 0.5, 0.9)
agent.train(10)
agent.play()

                      
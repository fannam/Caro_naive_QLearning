from engine import GameState
from const import *
import numpy as np

class QLearningAgent:
    def __init__(self, alpha, epsilon, discount_factor):
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.Q = {}
    
    def state_to_string(self, state):
        return str(state.board)

    def get_Q_value(self, state, action):
        state_str = self.state_to_string(state)
        return self.Q.get((state_str, action), np.random.uniform(-1.0, 1.0))
    
    def choose_action(self, state, avaiable_moves):
        if np.random.rand() < self.epsilon:
            index = np.random.choice(len(avaiable_moves))
            return avaiable_moves[index]
        else:
            Q_value = [self.get_Q_value(state, move) for move in avaiable_moves]
            return avaiable_moves[np.argmax(Q_value)]
    
    def update_Q_value(self, state, action, reward, next_state):
        state_str = self.state_to_string(state)
        best_next_Q = np.max([self.get_Q_value(next_state, move) for move in next_state.avaiable_moves()])
        current_Q_value = self.get_Q_value(state, action)
        new_Q_value = (1 - self.alpha) * current_Q_value + self.alpha * (reward + self.discount_factor * best_next_Q)
        self.Q[(state_str, action)] = new_Q_value

    def train(self, num_episodes):
        for episode in range(num_episodes):
            state = GameState()
            reward = 0
            while not state.isGameOver() and not state.isBoardFull():
                available_moves = state.avaiable_moves()
                if not available_moves:
                    break
                action = self.choose_action(state, available_moves)
                state.make_move(action)
                next_state = state
                self.update_Q_value(state, action, reward, next_state)
            if state.winner == 'X':
                reward = 1.0
            elif state.isBoardFull():
                reward = 0.0
            else:
                reward = -1.0
            
            # for row in state.board:
            #     print(row)
            print(f"Episode {episode + 1}/{num_episodes}, Winner: {state.winner}, Q-value updates: {len(self.Q)}")    
    def play(self):
        game = GameState()
        while not game.game_over:
            available_moves = game.avaiable_moves()
            action = self.choose_action(game, available_moves)
            game.make_move(action)
            for row in game.board:
                print(row)           
caro_ai = QLearningAgent(0.1, 0.3, 0.9)
caro_ai.train(5)
caro_ai.play()
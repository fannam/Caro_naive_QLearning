from engine import GameState  # Import your GameState class
import numpy as np
from const import *
class QLearning_version2:
    def __init__(self, player, alpha, epsilon, discount_factor):
        self.player = player
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.reward = 0.0
        self.Q = {}

    def state_to_string(self, state):
        return str(state.board)

    def get_Q_value(self, state, action):
        state_str = self.state_to_string(state)
        return self.Q.get((state_str, action), np.random.uniform(-0.1, 0.1))

    def choose_action(self, state, available_moves):
        if np.random.rand() < self.epsilon:
            index = np.random.choice(len(available_moves))
            return available_moves[index]
        else:
            Q_values = [self.get_Q_value(state, move) for move in available_moves]
            return available_moves[np.argmax(Q_values)]

    def update_Q_value(self, state, action, reward, next_state):
        state_str = self.state_to_string(state)
        best_next_Q = np.max([self.get_Q_value(next_state, move) for move in next_state.available_moves()])
        current_Q_value = self.get_Q_value(state, action)
        new_Q_value = (1 - self.alpha) * current_Q_value + self.alpha * (reward + self.discount_factor * best_next_Q)
        self.Q[(state_str, action)] = new_Q_value

    def best_move(self, state):
        available_moves = state.available_moves()
        if len(available_moves) == 0:
            return None  # No available moves
        Q_values = [self.get_Q_value(state, move) for move in available_moves]
        best_move_index = np.argmax(Q_values)
        return available_moves[best_move_index]

    def print_Q_value(self):
        for key, value in self.Q.items():
            print(f"Key: {key}, Value: {value}")

def train_agents(agent1, agent2, num_episodes):
    for episode in range(num_episodes):
        state = GameState()
        total_reward_agent1 = 0.0
        total_reward_agent2 = 0.0

        while not state.game_over:
            current_agent = agent1 if state.current_player == 'X' else agent2
            available_moves = state.available_moves()
            if len(available_moves)==0:
                    break
            # Choose action using epsilon-greedy strategy
            action = current_agent.choose_action(state, available_moves)
            current_state = state
            # Take the chosen action
            state.make_move(action, current_agent.player)
            next_state = state
            next_avaiable_moves = next_state.available_moves() 
            if next_state.isGameOver():
                if next_state.winner == agent1.player:
                    agent1.reward = 100.0
                    # agent2.reward = -100.0
                elif next_state.winner == agent2.player:
                    # agent1.reward = -100.0
                    agent2.reward = 100.0
            elif next_state.isBoardFull():
                current_agent.reward = 0.0
            else:       
            # Calculate the reward (you need to define this based on the game rules)
                current_agent.reward = current_state.evaluate_game_state_with_new_move_ver2(current_state.current_player, WINNING_COUNT)

            # Update Q-value for the current agent
            if next_avaiable_moves:
                current_agent.update_Q_value(current_state, action, current_agent.reward, next_state)

            # Update total reward for the current agent
            if current_agent.player == 'X':
                total_reward_agent1 += current_agent.reward
            else:
                total_reward_agent2 += current_agent.reward

        # Print or log the total rewards for the episode
        print(f"Episode {episode + 1}, Total Reward Agent X: {total_reward_agent1}, Total Reward Agent O: {total_reward_agent2}")

# agent_X = QLearningAgent(player='X', alpha=0.1, epsilon=0.1, discount_factor=0.9)
# agent_O = QLearningAgent(player='O', alpha=0.1, epsilon=0.1, discount_factor=0.9)

# train_agents(agent_X, agent_O, num_episodes=1000)
# agent_X.print_Q_value()
# agent_O.print_Q_value()

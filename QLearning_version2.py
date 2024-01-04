from engine import *  
import numpy as np
from const import *
import json
import pyodbc
import copy
class QLearning_version2:
    def __init__(self, player, alpha, epsilon, discount_factor, database_connection_string):
        self.player = player
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.reward = 0.0
        self.Q = {}
        self.connection_string = database_connection_string

    def connect_to_database(self):
        try:
            self.conn = pyodbc.connect(self.connection_string)
            self.cursor = self.conn.cursor()

            self.cursor.execute(f"""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'QValues_{self.player}')
                CREATE TABLE QValues_{self.player} (
                    state_str VARCHAR(1000) NOT NULL,
                    action_str VARCHAR(100) NOT NULL,
                    QValue FLOAT NOT NULL,
                    PRIMARY KEY (state_str, action_str)
                )
            """)
            self.conn.commit()

            print(f"Connected to the database successfully for Agent {self.player}.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def save_Q_values_to_database(self):
        self.connect_to_database()
        for (state_str, action_str), q_value in self.Q.items():
            self.cursor.execute(
                f"""
                MERGE INTO QValues_{self.player} AS target
                USING (VALUES (?, ?, ?)) AS source (state_str, action_str, QValue)
                ON target.state_str = source.state_str AND target.action_str = source.action_str
                WHEN MATCHED THEN
                    UPDATE SET QValue = source.QValue
                WHEN NOT MATCHED THEN
                    INSERT (state_str, action_str, QValue) VALUES (source.state_str, source.action_str, source.QValue);
                """,
                state_str, action_str, q_value
            )

        self.conn.commit()
        self.close_database_connection()
    def load_Q_values_from_database(self):
        self.connect_to_database()

        self.cursor.execute(f"SELECT state_str, action_str, QValue FROM QValues_{self.player}")
        rows = self.cursor.fetchall()
        
        for row in rows:
            state_str, action_str, q_value = row
            self.Q[(state_str, action_str)] = q_value
        self.close_database_connection()

    def close_database_connection(self):
        if hasattr(self, 'conn') and self.conn and not self.conn.closed:
            self.conn.close()
###########################
    def state_to_string(self, state):
        state_dict = {
            'board': state.board,
            'current_player': state.current_player
        }
        return json.dumps(state_dict)

    def action_to_string(self, action):
        return f"{action[0]},{action[1]}"

    def get_Q_value(self, state, action):
        state_str = self.state_to_string(state)
        action_str = self.action_to_string(action)
        return self.Q.get((state_str, action_str), np.random.uniform(-0.1, 0.1))

    def choose_action(self, state, available_moves):
        if np.random.rand() < self.epsilon:
            index = np.random.choice(len(available_moves))
            return available_moves[index]
        else:
            Q_values = [self.get_Q_value(state, move) for move in available_moves]
            return available_moves[np.argmax(Q_values)]

    def update_Q_value(self, state, action, reward, next_state):
        state_str = self.state_to_string(state)
        action_str = self.action_to_string(action)
        best_next_Q = np.max([self.get_Q_value(next_state, move) for move in next_state.valid_neighbour_moves()])
        current_Q_value = self.get_Q_value(state, action)
        new_Q_value = (1 - self.alpha) * current_Q_value + self.alpha * (reward + self.discount_factor * best_next_Q)
        self.Q[(state_str, action_str)] = new_Q_value

    def best_move(self, state):
        available_moves = state.valid_neighbour_moves()
        if len(available_moves) == 0:
            return None  # No available moves
        temp_state = copy.deepcopy(state)
        best_move = check_winning_move(temp_state)
        if best_move == None:
            best_move = check_has_to_block(temp_state)
            if best_move == None:
                Q_values = [self.get_Q_value(state, move) for move in available_moves]
                best_move_index = np.argmax(Q_values)
                print(f"{self.state_to_string(state)} {available_moves[best_move_index]} {self.get_Q_value(state, available_moves[best_move_index])}")
                return available_moves[best_move_index]
            else:
                return best_move
        else:
            return best_move

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
            available_moves = state.valid_neighbour_moves()
            if len(available_moves)==0:
                    break
            action = current_agent.choose_action(state, available_moves)
            if action != state.get_best_move():
                current_agent.reward = -10.0
            else:
                current_agent.reward = 10.0
            current_state = copy.deepcopy(state)   
            #print(f"agent1 state {agent1.state_to_string(current_state)}")     
            state.make_move(action, current_agent.player)
            #print(f"agent1 state after state.makemove {agent1.state_to_string(current_state)}")
            next_state = copy.deepcopy(state)
            next_avaiable_moves = next_state.valid_neighbour_moves() 
            if next_state.isGameOver():
                if next_state.winner == agent1.player:
                    agent1.reward = 1000.0
                elif next_state.winner == agent2.player:
                    agent2.reward = 1000.0
            elif next_state.isBoardFull():
                current_agent.reward = 0.0
            #print(current_agent.state_to_string(current_state))
            if next_avaiable_moves:
                if current_agent == agent1:

                    #print(f"agent1 state {agent1.state_to_string(current_state)}")
                    agent1.update_Q_value(current_state, action, current_agent.reward, next_state)
                else:
                    agent2.update_Q_value(current_state, action, current_agent.reward, next_state)
                
                

            if current_agent.player == 'X':
                total_reward_agent1 += current_agent.reward
            else:
                total_reward_agent2 += current_agent.reward

        # Print or log the total rewards for the episode
        print(f"Episode {episode + 1}, Winner: {state.winner} Total Reward Agent X: {total_reward_agent1}, Total Reward Agent O: {total_reward_agent2}")
        
agent_X = QLearning_version2('X', 0.1, 0.1, 0.9, "DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\mssqllocaldb;DATABASE=CaroQValues;Trusted_Connection=yes;")
agent_O = QLearning_version2('O', 0.1, 0.1, 0.9, "DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\mssqllocaldb;DATABASE=CaroQValues;Trusted_Connection=yes;")

agent_O.load_Q_values_from_database()
agent_X.load_Q_values_from_database()
train_agents(agent_X, agent_O, num_episodes=1000)
agent_O.save_Q_values_to_database()
agent_X.save_Q_values_to_database()


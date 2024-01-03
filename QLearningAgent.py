from engine import GameState
from const import *
import numpy as np
import pyodbc
import json

class QLearningAgent:
    def __init__(self, alpha, epsilon, discount_factor, database_connection_string):
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

            self.cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'QValues')
                CREATE TABLE QValues (
                    state_str VARCHAR(1000) NOT NULL,
                    action_str VARCHAR(100) NOT NULL,
                    QValue FLOAT NOT NULL,
                    PRIMARY KEY (state_str, action_str)
                )
            """)
            self.conn.commit()

            print("Connected to the database successfully.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def save_Q_values_to_database(self):
        self.connect_to_database()

        values = [(state_str, action_str, q_value) for (state_str, action_str), q_value in self.Q.items()]

        self.cursor.executemany(
            """
            MERGE INTO QValues AS target
            USING (VALUES (?, ?, ?)) AS source (state_str, action_str, QValue)
            ON target.state_str = source.state_str AND target.action_str = source.action_str
            WHEN MATCHED THEN
                UPDATE SET QValue = source.QValue
            WHEN NOT MATCHED THEN
                INSERT (state_str, action_str, QValue) VALUES (source.state_str, source.action_str, source.QValue);
            """,
            values
        )

        self.conn.commit()
        self.close_database_connection()


    def load_Q_values_from_database(self):
        self.connect_to_database()

        self.cursor.execute("SELECT state_str, action_str, QValue FROM QValues")
        rows = self.cursor.fetchall()
        
        for row in rows:
            state_str, action_str, q_value = row
            self.Q[(state_str, action_str)] = q_value
        self.close_database_connection()
    def close_database_connection(self):
        if hasattr(self, 'conn') and self.conn and not self.conn.closed:
            self.conn.close()

    ###############################
    def state_to_string(self, state):
        state_dict = {
            'board': state.board,
            'current_player': state.current_player
        }
        return json.dumps(state_dict)

    def action_to_string(self, action):
        return f"{action[0]},{action[1]}"
    
    def action_str_to_action(self, action_str):
        row, col = map(int, action_str.split(','))
        return row, col
    
    def get_Q_value(self, state, action):
        state_str = self.state_to_string(state)
        action_str = self.action_to_string(action)
        return self.Q.get((state_str, action_str), np.random.uniform(-0.1, 0.1))#)
    
    def choose_action(self, state, available_moves):
        #print(self.state_to_string(state))
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
        action_str = self.action_to_string(action)
        if next_state.current_player == 'X':
            best_next_Q = np.max([self.get_Q_value(next_state, move) for move in next_state.available_moves()])
        elif next_state.current_player == 'O':
            best_next_Q = np.min([self.get_Q_value(next_state, move) for move in next_state.available_moves()])
        current_Q_value = self.get_Q_value(state, action)
        new_Q_value = (1 - self.alpha) * current_Q_value + self.alpha * (reward + self.discount_factor * best_next_Q)
        self.Q[(state_str, action_str)] = new_Q_value

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
                if action == state.get_best_move():
                    if state.current_player == 'X':
                        self.reward = 10.0
                    else:
                        self.reward = -10.0
                else:
                    if state.current_player == 'X':
                        self.reward = -10.0
                    else:
                        self.reward = 10.0
                
                current_state = state
                state.make_move(action, current_state.current_player)
                next_state = state
                next_avaiable_moves = next_state.available_moves()
                if next_avaiable_moves:
                    self.update_Q_value(current_state, action, self.reward, next_state)
                    #print(self.get_Q_value(current_state, action))
                if next_state.isGameOver():
                    if next_state.winner == 'X':
                        self.reward = 100.0
                    elif next_state.winner == 'O':
                        self.reward = -100.0
                elif next_state.isBoardFull():
                    self.reward = 0.0                     
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
        print(f"{self.state_to_string(state)} {available_moves[best_move_index]} {self.get_Q_value(state, available_moves[best_move_index])}")
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

# agent = QLearningAgent(0.1, 0.3, 0.9, "DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\mssqllocaldb;DATABASE=CaroQValues;Trusted_Connection=yes;")
# agent.load_Q_values_from_database()
# agent.train(10)
# agent.save_Q_values_to_database()





                      
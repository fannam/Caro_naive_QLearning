import pygame
import sys
import os
from const import *
from engine import GameState
from QLearningAgent import QLearningAgent
from tkinter import messagebox
from QLearning_version2 import *

class MainMenu:
    def __init__(self):
        self.game_mode = None

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caro AI Menu")

        # Load and scale the background image
        background_image = pygame.image.load(os.path.join('Images', 'background.jpg'))
        self.background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

        # Create buttons
        

    def load_background(self):
        pvp_button_rect = pygame.Rect((WIDTH // 2 - 250, HEIGHT // 4, 200, 50))
        pvcom_button_rect = pygame.Rect((WIDTH // 2 - 250, HEIGHT // 4 + 60, 200, 50))
        options_button_rect = pygame.Rect((WIDTH // 2 - 250, HEIGHT // 4 + 120, 200, 50))
        exit_button_rect = pygame.Rect((WIDTH // 2 - 250, HEIGHT // 4 + 180, 200, 50))
        
        choose_symbol_rect = pygame.Rect((WIDTH // 2, HEIGHT // 2, 200, 50))
        x_button_rect = pygame.Rect((WIDTH // 2 + 10, HEIGHT // 2 + 60, 40, 40))
        o_button_rect = pygame.Rect((WIDTH // 2 + 60, HEIGHT // 2 + 60, 40, 40))
        
        choose_symbol = False  # Variable to track if the user is choosing a symbol
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pvp_button_rect.collidepoint(event.pos):
                        self.game_mode = GameMode.PvP
                    elif pvcom_button_rect.collidepoint(event.pos):
                        choose_symbol = True 
                    elif options_button_rect.collidepoint(event.pos):
                        self.show_options()
                    elif exit_button_rect.collidepoint(event.pos):
                        self.exit_game()
                    
                    if choose_symbol:
                        if x_button_rect.collidepoint(event.pos):
                            self.game_mode = GameMode.PvComX
                        elif o_button_rect.collidepoint(event.pos):
                            self.game_mode = GameMode.PvComO

            self.screen.blit(self.background, (0, 0))

            pygame.draw.rect(self.screen, (255, 255, 255), pvp_button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), pvcom_button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), options_button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), exit_button_rect)
            
            if choose_symbol:
                pygame.draw.rect(self.screen, (255, 255, 255), choose_symbol_rect)
                pygame.draw.rect(self.screen, (255, 255, 255), x_button_rect)
                pygame.draw.rect(self.screen, (255, 255, 255), o_button_rect)
                
                font = pygame.font.Font(None, 36)
                choose_symbol_text = font.render("Choose Symbol", True, (0, 0, 0))
                x_text = font.render("X", True, (0, 0, 0))
                o_text = font.render("O", True, (0, 0, 0))
                
                self.screen.blit(choose_symbol_text, (WIDTH // 2 + 100 - choose_symbol_text.get_width() // 2, HEIGHT // 2 + 15))
                self.screen.blit(x_text, (x_button_rect.x + x_button_rect.width // 2 - x_text.get_width() // 2,
                                          x_button_rect.y + x_button_rect.height // 2 - x_text.get_height() // 2))
                self.screen.blit(o_text, (o_button_rect.x + o_button_rect.width // 2 - o_text.get_width() // 2,
                                          o_button_rect.y + o_button_rect.height // 2 - o_text.get_height() // 2))

            font = pygame.font.Font(None, 36)
            pvp_text = font.render("PvP Mode", True, (0, 0, 0))
            pvcom_text = font.render("PvCom Mode", True, (0, 0, 0))
            options_text = font.render("Options", True, (0, 0, 0))
            exit_text = font.render("Exit", True, (0, 0, 0))

            self.screen.blit(pvp_text, (WIDTH // 2 - 150 - pvp_text.get_width() // 2, HEIGHT // 4 + 15))
            self.screen.blit(pvcom_text, (WIDTH // 2 - 150 - pvcom_text.get_width() // 2, HEIGHT // 4 + 75))
            self.screen.blit(options_text, (WIDTH // 2 - 150 - options_text.get_width() // 2, HEIGHT // 4 + 135))
            self.screen.blit(exit_text, (WIDTH // 2 - 150 - exit_text.get_width() // 2, HEIGHT // 4 + 195))

            pygame.display.flip()

            if self.game_mode is not None:
                break

    def show_options(self):
        pass

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def get_game_mode(self):
        return self.game_mode


class GameMode:
    PvP = 1
    PvComX = 2 #người chơi là X
    PvComO = 3 #người chơi là O


class Main:
    def __init__(self, game_mode):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game_state = GameState()
        self.isPlayer1Turn = True
        self.isHumanTurn = False
        self.isAITurn = True
        self.images = {'X': None, 'O': None}
        self.loadImage()
        pygame.display.set_caption("Caro AI")
        self.game_mode = game_mode

    def loadImage(self):
        for symbol in self.images.keys():
            image_path = os.path.join(f'Images/{symbol}.png')
            self.images[symbol] = pygame.transform.smoothscale(pygame.image.load(image_path), (SQSIZE, SQSIZE))

    def drawBoard(self, screen):
        self.screen.fill((255, 255, 255))
        for i in range(ROWS):
            pygame.draw.line(screen, (0, 0, 0), (0, i * SQSIZE), (WIDTH, i * SQSIZE))
            pygame.draw.line(screen, (0, 0, 0), (i * SQSIZE, 0), (i * SQSIZE, HEIGHT))

    def drawObject(self):
        for row in range(ROWS):
            for col in range(COLS):
                obj = self.game_state.board[row][col]
                if obj == '--':
                    continue
                elif obj == 'X':
                    self.screen.blit(self.images[obj], (col * SQSIZE, row * SQSIZE))
                elif obj == 'O':
                    self.screen.blit(self.images[obj], (col * SQSIZE, row * SQSIZE))

    def drawGameState(self, screen):
        self.drawBoard(screen)
        self.drawObject()

    def show_game_over_message(self):
        if self.game_state.winner == 'X':
            result = messagebox.showinfo("Game Over", f"Game Over! Player X wins!")
        elif self.game_state.winner == 'O':
            result = messagebox.showinfo("Game Over", f"Game Over! Player O wins!")
        else:
            result = messagebox.showinfo("Game Over", "Game Over! It's a draw!")

        if result == 'ok':
            self.game_state = GameState()
            self.isPlayer1Turn = True
            self.drawGameState(self.screen)
            pygame.display.flip()

    def mainloop(self):
        in_game = True
        while in_game:
            game_running = True
            self.game_state = GameState()
            if self.game_mode == GameMode.PvComX:
                
                self.isHumanTurn = True
                self.drawGameState(self.screen)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                while game_running:
                    for event in pygame.event.get():                       
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                game_running = False
                                self.game_mode = None
                                in_game = False
                                break    
                            elif event.key == pygame.K_r:  
                                self.isHumanTurn = True
                                self.game_state = GameState()
                                self.drawGameState(self.screen)                             
                                pygame.display.flip()
                        elif event.type == pygame.MOUSEBUTTONDOWN and self.isHumanTurn:
                            location = pygame.mouse.get_pos()
                            col = location[0] // SQSIZE
                            row = location[1] // SQSIZE
                            if self.game_state.isValidMove(row, col) and not self.game_state.isGameOver():
                                self.game_state.board[row][col] = 'X'
                                self.drawGameState(self.screen)
                                pygame.display.flip()
                                self.isHumanTurn = False
                                agent_move = agent_X.best_move(self.game_state)
                                #agent_move = agent.best_move(self.game_state)
                                if not self.game_state.isGameOver():
                                    if not self.game_state.isBoardFull():
                                        agent_row, agent_col = agent_move
                                        self.game_state.board[agent_row][agent_col] = 'O'
                                        self.drawGameState(self.screen)
                                        pygame.display.flip()
                                        self.isHumanTurn = True
                    if self.game_state.isBoardFull() or self.game_state.isGameOver():
                        game_running = False  
                        self.show_game_over_message()              
            elif self.game_mode == GameMode.PvComO:              
                self.isAITurn = True
                self.drawGameState(self.screen)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                while game_running:
                    for event in pygame.event.get():                       
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                game_running = False
                                self.game_mode = None
                                in_game = False
                                break    
                            elif event.key == pygame.K_r:  
                                self.isAITurn = True
                                self.game_state = GameState()
                                self.drawGameState(self.screen)                             
                                pygame.display.flip()
                        elif event.type == pygame.MOUSEBUTTONDOWN and not self.isAITurn:
                            location = pygame.mouse.get_pos()
                            col = location[0] // SQSIZE
                            row = location[1] // SQSIZE
                            if self.game_state.isValidMove(row, col) and not self.game_state.isGameOver():
                                self.game_state.board[row][col] = 'O'
                                self.drawGameState(self.screen)
                                pygame.display.flip()
                                self.isAITurn = True                        
                    if self.isAITurn:
                        agent_move = agent_O.best_move(self.game_state)
                        #agent_move = agent.best_move(self.game_state)
                        if not self.game_state.isGameOver():
                            if not self.game_state.isBoardFull():
                                agent_row, agent_col = agent_move
                                self.game_state.board[agent_row][agent_col] = 'X'
                                self.drawGameState(self.screen)
                                pygame.display.flip()
                                self.isAITurn = False
                        elif self.game_state.isGameOver() or self.game_state.isBoardFull():
                            game_running = False  
                            self.show_game_over_message()
                    elif self.game_state.isGameOver() or self.game_state.isBoardFull():
                        game_running = False  
                        self.show_game_over_message()        
            elif self.game_mode == GameMode.PvP:
                print("PVP mode")
                self.drawGameState(self.screen)
                pygame.display.flip()       
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                while game_running:
                    for event in pygame.event.get():                       
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                game_running = False
                                self.game_mode = None
                                in_game = False
                                break    
                            elif event.key == pygame.K_r:  
                                self.isPlayer1Turn = True
                                self.game_state = GameState()
                                self.drawGameState(self.screen)                             
                                pygame.display.flip()      
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            location = pygame.mouse.get_pos()
                            col = location[0] // SQSIZE
                            row = location[1] // SQSIZE
                            if self.game_state.isValidMove(row, col):
                                self.game_state.board[row][col] = self.game_state.current_player
                                self.drawGameState(self.screen)
                                pygame.display.flip()
                                self.game_state.switch_player()
                        
                    if self.game_state.isBoardFull() or self.game_state.isGameOver():
                        game_running = False  
                        self.show_game_over_message()         

localdb_connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\\mssqllocaldb;DATABASE=CaroQValues;Trusted_Connection=yes;"

agent = QLearningAgent(0.1, 0.3, 0.9, localdb_connection_string)
agent_X = QLearning_version2(player='X', alpha=0.1, epsilon=0.1, discount_factor=0.9)
agent_O = QLearning_version2(player='O', alpha=0.1, epsilon=0.1, discount_factor=0.9)
if __name__ == "__main__":
    agent.load_Q_values_from_database()
    while True:
        menu = MainMenu()
        menu.load_background()
        game_mode = menu.get_game_mode()

        if game_mode:
            if game_mode == GameMode.PvComO:
                game = Main(game_mode)
                game.mainloop()
            elif game_mode == GameMode.PvComX:
                game = Main(game_mode)
                game.mainloop()
            elif game_mode == GameMode.PvP:
                game = Main(game_mode)
                game.mainloop()

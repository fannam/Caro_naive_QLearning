import pygame
import sys
import os
from const import *
from engine import GameState
from QLearningAgent import QLearningAgent

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.playerClicked = []
        self.selectedSquare = ()
        self.game_state = GameState()
        self.agent = QLearningAgent(0.2, 0.15, 0.99)
        self.agent.train(10000)
        self.isPlayer1Turn = True
        self.isHumanTurn = False
        self.isAITurn = True
        self.images = {'X': None, 'O': None}
        self.loadImage()
        pygame.display.set_caption("Caro AI")

    def loadImage(self):
        for symbol in self.images.keys():
            image_path = os.path.join(f'Images/{symbol}.png')
            self.images[symbol] = pygame.transform.smoothscale(pygame.image.load(image_path), (SQSIZE, SQSIZE))


    def drawBoard(self, screen):
        self.screen.fill((255, 255, 255))
        for i in range (ROWS):
            pygame.draw.line(screen, (0, 0, 0), (0, i * SQSIZE), (WIDTH, i * SQSIZE))
            pygame.draw.line(screen, (0, 0, 0), (i * SQSIZE, 0), (i * SQSIZE, HEIGHT))
            
    def drawObject(self, board):
        for row in range(ROWS):
            for col in range(COLS):
                obj = board[row][col]
                if obj == '--':
                    continue
                elif obj == 'X':
                    self.screen.blit(self.images[obj], (col * SQSIZE, row * SQSIZE))
                elif obj == 'O':
                    self.screen.blit(self.images[obj], (col * SQSIZE, row * SQSIZE))

    def drawGameState(self, screen, game_state):
        self.drawBoard(screen)
        self.drawObject(game_state.board)
        pygame.display.flip()

    def mainloop(self):
        self.drawBoard(self.screen)
        pygame.display.flip()
        while True:
            self.drawGameState(self.screen, self.game_state)
            
            if self.isAITurn and not (self.game_state.isGameOver() or self.game_state.isBoardFull()):
                AI_best_move = self.agent.best_move(self.game_state)
                AI_row, AI_col = AI_best_move
                self.game_state.board[AI_row][AI_col] = 'X'
                self.isAITurn = False
                self.isHumanTurn = True
                self.drawBoard(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    col = location[0]//SQSIZE
                    row = location[1]//SQSIZE
                    if self.game_state.isValidMove(row, col) and not self.game_state.isGameOver():
                        self.game_state.board[row][col] = 'O'
                        self.isAITurn = True
                        self.isHumanTurn = False
                #     #self.selectedSquare(row, col)
                #     if self.isHumanTurn and not self.game_state.isGameOver() and self.game_state.isValidMove(row, col):
                #         self.game_state.board[row][col] = 'X'
                #         AI_best_move = self.agent.best_move(self.game_state)
                #         if not self.game_state.isGameOver():
                #             if not self.game_state.isBoardFull():
                #                 AI_row, AI_col = AI_best_move
                #                 self.game_state.board[AI_row][AI_col] = 'O'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_state = GameState()   
                        self.isAITurn = True
                        self.isHumanTurn = False    

                    

                
main = Main()
main.mainloop()
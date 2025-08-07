import pygame
import math
import sys

#init game
pygame.init()

#Constant
WINDOW_SIZE = 800
BOARD_SIZE = 5
TILE_SIZE = WINDOW_SIZE / (BOARD_SIZE + 2)
BOARD_OFFSET = TILE_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_RED = (255, 150, 150)
LIGHT_BLUE = (150, 150, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class TileCaptureGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Tile Capture Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 36)

        #Game state
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 1
        self.game_over = False
        self.valid_move = set()
        self.last_move = None
        self.player1_score = 0
        self.player2_score = 0

    def get_surrounding_positions(self, x, y):
        surrounding_positions = []
        for dr in [-1,0,1]: #delta row: up/same/dowm
            for dc in [-1,0,1]: #delta column: left/same/right
                # if dr == 0 and dc == 0:
                #     continue
                new_row, new_col = x + dr, y + dc
                if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                    surrounding_positions .append((new_row, new_col))
        return surrounding_positions

    def get_adjacent_positions(self, x, y):
        adjacent_positions =[]
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            new_row, new_col = x + dr, y + dc
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                adjacent_positions .append((new_row, new_col))
        return adjacent_positions

    def get_valid_moves(self):
        self.valid_move.clear()
        if self.last_move is None:
            #first tiles all valid
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    self.valid_move.add((row, col))

        else:
            last_row, last_col = self.last_move
            adjacent = self.get_adjacent_positions(last_row, last_col)

            for row, col in adjacent:
                if self.board[row][col] is None:
                    self.valid_move.add((row, col))

    def count_surrounding_tile(self, x, y,player):
        count = 0
        surrounding = self.get_surrounding_positions(x, y)
        for sr, sc in surrounding:
            if self.board[sr][sc] == player:
                count += 1
        return count




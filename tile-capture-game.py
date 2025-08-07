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

    def make_move(self,row,col):
        if (row, col) not in self.valid_move:
            return False
        #place
        self.board[row][col] = self.current_player
        self.last_move = (row, col)

        #check capture
        self.check_captures(row, col)

        #switch player
        self.current_player = 3 - self.current_player

        #update valid move for next player
        self.get_valid_moves()

        #check if game is over
        if len(self.valid_move) == 0:
            self.game_over = True
            self.calculate_final_scores()

        return True

    def check_captures(self, row, col):
        surrounding = self.get_surrounding_positions(row, col)
        for sr, sc in surrounding:
            if self.board[sr][sc] is not None and self.board[sr][col] != self.current_player:
                current_surrounding = self.count_surrounding_tile(sr, sc, self.current_player)
                opponent_surrounding = self.count_surrounding_tile(sr, -sc, self.board[sr][sc])
                if current_surrounding > opponent_surrounding:
                    self.board[sr][sc] = self.current_player

    def calculate_final_scores(self):
        self.player1_score = sum(1 for row in self.board for tile in row if tile == 1 )
        self.player2_score = sum(1 for row in self.board for tile in row if tile == 2 )

    def get_tile_color(self, row, col):
        if self.board[row][col] is None:
            if (row,col) in self.valid_move:
                return LIGHT_GRAY
            else:
                return WHITE
        elif self.board[row][col] == 1:
            return RED
        else:
            return BLUE

    def draw_board(self):
        self.screen.fill(WHITE)

        #tiles
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = BOARD_OFFSET + col * TILE_SIZE
                y = BOARD_OFFSET + row * TILE_SIZE

                color = self.get_tile_color(row, col)
                pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, BOARD_SIZE),2)

                if (row, col) in self.valid_move:
                    center_x = x + TILE_SIZE//2
                    center_y = y + TILE_SIZE//2
                    pygame.draw.circle(self.screen, GREEN, (center_x, center_y), TILE_SIZE//2)

        player_text = f"Player {self.current_player}'s Turn"
        player_color = RED if self.current_player == 1 else BLUE
        text_surface = self.font.render(player_text, True, player_color)
        text_rect = text_surface.get_rect(center= (WINDOW_SIZE//2, 30))
        self.screen.blit(text_surface, text_rect)

        if self.game_over:
            winner = "Player 1" if self.player1_score > self.player2_score else "Player 2"
            if self.player1_score == self.player2_score:
                winner = "Tie"

            game_over_text = f"Game Over: {winner} wins"
            game_over_surface = self.font.render(game_over_text, True, player_color)
            game_over_rect = game_over_surface.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))

            pygame.draw.rect(self.screen, WHITE, game_over_rect.inflate(20,20))
            pygame.draw.rect(self.screen, WHITE, game_over_rect.inflate(20,20),2)
            self.screen.blit(game_over_surface, game_over_rect)

    def handle_click(self, pos):
        if self.game_over:
            return
        x,y = pos
        col = (x - BOARD_OFFSET)//TILE_SIZE
        row = (y - BOARD_OFFSET) // TILE_SIZE

        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            self.make_move(row, col)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()

            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    game = TileCaptureGame()
    game.run()




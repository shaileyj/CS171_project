#Team Members: Shailey Joseph, My Nguyen
import pygame
import sys

#init game
pygame.init()

#Constant
WINDOW_SIZE = 800
WINDOW_HEIGHT = 800
BOARD_SIZE = 5
TILE_SIZE = WINDOW_SIZE / (BOARD_SIZE + 2)
BOARD_OFFSET = TILE_SIZE
ANNOTATION_WIDTH = 350

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
    def __init__(self, screen):
        self.screen = screen #pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
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

        #track moves
        self.player1_moves = []
        self.player2_moves = []
        self.player1_valid_moves = set()
        self.player2_valid_moves = set()

        # Initialize valid moves for both players
        self.update_all_valid_moves()

    def update_all_valid_moves(self):
        """Update valid moves for both players"""
        self.update_player_valid_moves(1)
        self.update_player_valid_moves(2)

    def update_player_valid_moves(self, player):
        """Update valid moves for a specific player"""
        valid_moves = set()
        player_moves = self.player1_moves if player == 1 else self.player2_moves

        # Check if board is completely empty
        board_empty = all(self.board[row][col] is None
                          for row in range(BOARD_SIZE)
                          for col in range(BOARD_SIZE))

        if board_empty:
            # First move of the game - all tiles are valid
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    valid_moves.add((row, col))
        elif len(player_moves) == 0:
            # This player's first move - can place anywhere empty
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if self.board[row][col] is None:
                        valid_moves.add((row, col))
        else:
            # Find all adjacent positions to ALL of this player's existing tiles
            for move_row, move_col in player_moves:
                # Only consider tiles that are still owned by this player
                if self.board[move_row][move_col] == player:
                    adjacent = self.get_adjacent_positions(move_row, move_col)
                    for adj_row, adj_col in adjacent:
                        if self.board[adj_row][adj_col] is None:
                            valid_moves.add((adj_row, adj_col))

        # Update the appropriate valid moves set
        if player == 1:
            self.player1_valid_moves = valid_moves
        else:
            self.player2_valid_moves = valid_moves

    def get_current_valid_moves(self):
        """Get valid moves for the current player"""
        return self.player1_valid_moves if self.current_player == 1 else self.player2_valid_moves

    def get_adjacent_positions(self, x, y):
        adjacent_positions =[]
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            new_row, new_col = x + dr, y + dc
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                adjacent_positions .append((new_row, new_col))
        return adjacent_positions

    def get_valid_moves(self):
        self.valid_move.clear()

        board_empty = all(self.board[row][col] is None
                      for row in range(BOARD_SIZE)
                      for col in range(BOARD_SIZE))
        if board_empty:
            #first tiles all valid
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    self.valid_move.add((row, col))

        else:
            current_player_moves = self.player1_moves if self.current_player == 1 else self.player2_moves

            if self.last_move is None:
                for row in range(BOARD_SIZE):
                    for col in range(BOARD_SIZE):
                        if self.board[row][col] is None:
                            self.valid_move.add((row, col))
            else:
                # Find all adjacent positions to ALL of this player's existing tiles
                for move_row, move_col in current_player_moves:
                    # Only consider tiles that are still owned by this player
                    # (in case they were captured)
                    if self.board[move_row][move_col] == self.current_player:
                        adjacent = self.get_adjacent_positions(move_row, move_col)
                        for adj_row, adj_col in adjacent:
                            if self.board[adj_row][adj_col] is None:
                                self.valid_move.add((adj_row, adj_col))

    def count_adjacent_tile(self, x, y,player):
        count = 0
        surrounding = self.get_adjacent_positions(x, y)
        for sr, sc in surrounding:
            if self.board[sr][sc] == player:
                count += 1
        return count

    def make_move(self, row, col):
        current_valid_moves = self.get_current_valid_moves()

        if (row, col) not in current_valid_moves:
            print("Invalid move")
            return False

        # Place piece
        self.board[row][col] = self.current_player
        self.last_move = (row, col)

        # Add this move to the current player's move list
        if self.current_player == 1:
            self.player1_moves.append((row, col))
        else:
            self.player2_moves.append((row, col))

        # Check capture
        self.check_captures(row, col)

        # Check if board is full
        if self.is_board_full():
            self.game_over = True
            self.calculate_final_scores()
            return True

        # Switch player
        self.current_player = 3 - self.current_player

        # Update valid moves for both players
        self.update_all_valid_moves()

        # Check if current player has no valid moves
        current_valid_moves = self.get_current_valid_moves()
        if len(current_valid_moves) == 0:
            # Check if other player has moves
            other_player = 3 - self.current_player
            other_valid_moves = self.player1_valid_moves if other_player == 1 else self.player2_valid_moves

            if len(other_valid_moves) == 0:
                # Neither player can move - game over
                self.game_over = True
                self.calculate_final_scores()
            else:
                # Skip to other player
                print(f"Player {self.current_player} has no valid moves. Skipping turn.")
                self.current_player = other_player

        return True

    def is_board_full(self):
        """Check if all tiles on the board are occupied"""
        return all(self.board[row][col] is not None
                   for row in range(BOARD_SIZE)
                   for col in range(BOARD_SIZE))

    def check_captures(self, row, col):
        surrounding = self.get_adjacent_positions(row, col)
        for sr, sc in surrounding:
            if self.board[sr][sc] is not None and self.board[sr][sc] != self.current_player:
                current_surrounding = self.count_adjacent_tile(sr, sc, self.current_player)
                opponent_surrounding = self.count_adjacent_tile(sr, -sc, self.board[sr][sc])
                if current_surrounding > 1:
                    self.board[sr][sc] = self.current_player

    def calculate_final_scores(self):
        self.player1_score = sum(1 for row in self.board for tile in row if tile == 1 )
        self.player2_score = sum(1 for row in self.board for tile in row if tile == 2 )

    def get_tile_color(self, row, col):
        if self.board[row][col] is None:
            # if (row,col) in self.valid_move:
            #     return LIGHT_GRAY
            # else:
            return WHITE
        elif self.board[row][col] == 1:
            return RED
        else:
            return BLUE

    def draw_annotation(self):
        """Draw the game rules annotation on the right side"""
        # Title
        title_text = "GAME RULES"
        title_surface = self.font.render(title_text, True, BLACK)
        title_rect = title_surface.get_rect(centerx=1000 + ANNOTATION_WIDTH // 2, y=30)
        self.screen.blit(title_surface, title_rect)

        # Rules text - split into lines
        rules = [
            "1. Choose a tile adjacent to your",
            "   previous tiles (left/right/top/bottom)",
            "",
            "2. You can capture opponent's tiles",
            "   if you have more adjacent tiles",
            "   than the opponent has",
            "",
            "3. Winner has the greater number",
            "   of tiles when no empty tiles",
            "   are left",
            ""
        ]
        y_offset = 80
        line_height = 25

        for line in rules:
            if line.strip():  # Skip empty lines for spacing
                # Color code the player scores
                if "Player 1" in line:
                    text_surface = self.small_font.render(line, True, RED)
                elif "Player 2" in line:
                    text_surface = self.small_font.render(line, True, BLUE)
                else:
                    text_surface = self.small_font.render(line, True, BLACK)
                self.screen.blit(text_surface, (1020, y_offset))
            y_offset += line_height

    def draw_board(self):
        self.screen.fill(WHITE)

        self.draw_annotation()

        # Get current player's valid moves
        current_valid_moves = self.get_current_valid_moves()

        #tiles
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = BOARD_OFFSET + col * TILE_SIZE
                y = BOARD_OFFSET + row * TILE_SIZE

                color = self.get_tile_color(row, col)
                pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, TILE_SIZE))
        #grid
        for col in range(BOARD_SIZE+1): #vertical
            x = BOARD_OFFSET + col * TILE_SIZE
            pygame.draw.line(self.screen, BLACK,(x, BOARD_OFFSET),(x,BOARD_OFFSET+BOARD_SIZE*TILE_SIZE),2)
        for row in range(BOARD_SIZE + 1):  # horizontal
            y = BOARD_OFFSET + row * TILE_SIZE
            pygame.draw.line(self.screen, BLACK, (BOARD_OFFSET, y), (BOARD_OFFSET + BOARD_SIZE * TILE_SIZE, y), 2)

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
            print("Game is over!")
            return

        x, y = pos
        print(f"Click at position: ({x}, {y})")

        # Calculate which tile was clicked
        col = int( (x - BOARD_OFFSET) / TILE_SIZE)
        row = int( (y - BOARD_OFFSET) / TILE_SIZE)
        print(f"Calculated tile: row={row}, col={col}")

        # Check if click is within board bounds
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            print(f"Board state before: {self.board[row][col]}")

            # Try to make the move
            if self.make_move(row, col):
                print(f"Move successful! Board state after: {self.board[row][col]}")
                print(f"Current player now: {self.current_player}")
            else:
                print(f"Move failed - tile already occupied")
        else:
            print(f"Click outside board bounds")

    def run(self):
        running = True

        while running:
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # self.handle_click(event.pos)
                    self.handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
            if self.game_over:
                running = False
            # self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)

        #pygame.quit()
        #sys.exit()

def draw_board(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = BOARD_OFFSET + col * TILE_SIZE
            y = BOARD_OFFSET + row * TILE_SIZE

            if self.board[row][col] is None:
                # if (row,col) in self.valid_move:
                #     return LIGHT_GRAY
                # else:
                color = WHITE
            elif self.board[row][col] == 1:
                color = RED
            else:
                return BLUE
            color = self.get_tile_color(row, col)
            pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, TILE_SIZE))
            # pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, BOARD_SIZE),2)

            # if (row, col) in self.valid_move:
            #     center_x = x + TILE_SIZE//2
            #     center_y = y + TILE_SIZE//2
            #     pygame.draw.circle(self.screen, GREEN, (center_x, center_y), TILE_SIZE//2)
    # grid
    for col in range(BOARD_SIZE + 1):  # vertical
        x = BOARD_OFFSET + col * TILE_SIZE
        pygame.draw.line(self.screen, BLACK, (x, BOARD_OFFSET), (x, BOARD_OFFSET + BOARD_SIZE * TILE_SIZE), 2)
    for row in range(BOARD_SIZE + 1):  # horizontal
        y = BOARD_OFFSET + row * TILE_SIZE
        pygame.draw.line(self.screen, BLACK, (BOARD_OFFSET, y), (BOARD_OFFSET + BOARD_SIZE * TILE_SIZE, y), 2)

    def simple_heuristic(self):
        heuristic = []
        copy_valid_moves = list(self.player1_valid_moves)

        for move in copy_valid_moves:
            # Save COMPLETE current state
            original_board = [row[:] for row in self.board]
            original_player1_moves = self.player1_moves[:]
            original_player2_moves = self.player2_moves[:]
            original_player1_valid_moves = self.player1_valid_moves.copy()
            original_player2_valid_moves = self.player2_valid_moves.copy()
            original_current_player = self.current_player
            original_last_move = self.last_move

            # Ensure we're evaluating Player 1 moves
            self.current_player = 1

            trial = self.make_move(*move)

            if trial:
                # Calculate heuristic using NEW state (after move)
                player1_pieces = len(self.player1_moves)  # ← Use self, not copy
                player2_pieces = len(self.player2_moves)  # ← Use self, not copy
                player1_moves_count = len(self.player1_valid_moves)  # ← Use self, not copy
                player2_moves_count = len(self.player2_valid_moves)  # ← Use self, not copy

                heuristic_value = player1_pieces + player1_moves_count - player2_pieces - player2_moves_count
                heuristic.append(heuristic_value)

            # RESTORE original state
            self.board = original_board
            self.player1_moves = original_player1_moves
            self.player2_moves = original_player2_moves
            self.player1_valid_moves = original_player1_valid_moves
            self.player2_valid_moves = original_player2_valid_moves
            self.current_player = original_current_player
            self.last_move = original_last_move

        return heuristic
if __name__ == "__main__":
    game = TileCaptureGame()
    game.run()




import copy

import pygame
import sys

from minimax import simple_heuristic
import minimax

#init game
pygame.init()

#Constant
WINDOW_SIZE = 800
BOARD_SIZE = 5
TILE_SIZE = WINDOW_SIZE / (BOARD_SIZE + 2)
BOARD_OFFSET = TILE_SIZE
MAX_DISTANCE = 2

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

class GameWithHeuristic:
    def __init__(self):
        # Initialize pygame and game components
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption(f"Tile Capture Game")
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
        self.heuristic_choice = self.choose_heuristic()

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

    def count_adjacent_tile(self, x, y, player):
        count = 0
        surrounding = self.get_adjacent_positions(x, y)
        for sr, sc in surrounding:
            if self.board[sr][sc] == player:
                count += 1
        return count

    def count_adjacent_other_tile(self, x, y, player):
        count = 0
        surrounding = self.get_adjacent_positions(x, y)
        for sr, sc in surrounding:
            if self.board[sr][sc] is not None and self.board[sr][sc] != player:
                count += 1
        return count

    def make_move(self, row, col):
        # print(f"In make: Row: {row}, Col: {col}")
        current_valid_moves = self.get_current_valid_moves()

        if (row, col) not in current_valid_moves:
            # print("Invalid move")
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

        # Update valid moves for both players
        self.update_all_valid_moves()

        # # Choose heuristic function
        # if self.current_player == 1 and self.board is not None:
        #     self.choose_heuristic()

        # Switch player
        self.current_player = 3 - self.current_player

        # Check if current player has no valid moves
        current_valid_moves = self.get_current_valid_moves()

        if len(current_valid_moves) == 0:
            # Check if other player has moves
            other_player = 3 - self.current_player
            other_valid_moves = self.player1_valid_moves if other_player == 1 else self.player2_valid_moves

            if len(other_valid_moves) == 0:
                # Neither player can move - game over
                self.calculate_final_scores()
                self.game_over = True

        return True

    def is_board_full(self):
        """Check if all tiles on the board are occupied"""
        return all(self.board[row][col] is not None
                   for row in range(BOARD_SIZE)
                   for col in range(BOARD_SIZE))

    def check_captures(self, row, col): #if making move at row col, then can I capture any tiles
        surrounding_tile = self.get_adjacent_positions(row, col)
        for sr, sc in surrounding_tile:
            if self.board[sr][sc] is not None and self.board[sr][sc] != self.current_player:
                current_surrounding = self.count_adjacent_tile(sr, sc, self.current_player)

                if current_surrounding > 1:
                    self.board[sr][sc] = self.current_player
                    self.player1_moves.append((sr,sc))

    def early_termination(self):
        if len(self.player1_valid_moves) == 0 or len(self.player2_valid_moves) == 0:
            return True
        return False

    def calculate_final_scores(self):
        self.player1_score = sum(1 for row in self.board for tile in row if tile == 1 )
        self.player2_score = sum(1 for row in self.board for tile in row if tile == 2 )

    def get_tile_color(self, row, col):
        if self.board[row][col] is None:
            return WHITE
        elif self.board[row][col] == 1:
            return RED
        else:
            return BLUE

    def draw_board(self):
        self.screen.fill(WHITE)

        # Get current player's valid moves
        current_valid_moves = self.get_current_valid_moves()

        #tiles
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = BOARD_OFFSET + col * TILE_SIZE
                y = BOARD_OFFSET + row * TILE_SIZE

                color = self.get_tile_color(row, col)
                pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, TILE_SIZE))

                #draw heuristic value on empty tiles
                if self.current_player == 1 and self.board[row][col] is None and (row, col) in current_valid_moves:
                    heuristic_value = self.get_heuristic_value_for_tile(row, col)
                    if heuristic_value is not None:
                        # Format the heuristic value
                        if isinstance(heuristic_value, float):
                            text = f"{heuristic_value:.1f}"
                        else:
                            text = str(heuristic_value)

                        # Create text surface
                        text_surface = self.small_font.render(text, True, LIGHT_GRAY)
                        text_rect = text_surface.get_rect()
                        text_rect.center = (x + TILE_SIZE / 2, y + TILE_SIZE / 2)
                        self.screen.blit(text_surface, text_rect)
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
            if self.player1_score > self.player2_score:
                winner = "Player 1"
                winner_color = RED
                winner_text = f"Player 1 Wins!"
            elif self.player2_score > self.player1_score:
                winner = "Player 2"
                winner_color = BLUE
                winner_text = f"Player 2 Wins!"
            else:
                winner = "Tie"
                winner_color = BLACK
                winner_text = f"It's a Tie!"
            self.early_termination()

            # Create game over overlay
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
            overlay.set_alpha(128)  # Semi-transparent
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            # Main winner text
            winner_surface = pygame.font.Font(None, 72).render(winner_text, True, winner_color)
            winner_rect = winner_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))

            pygame.draw.rect(self.screen, LIGHT_GRAY, winner_rect.inflate(40, 40))

            # Blit all text
            self.screen.blit(winner_surface, winner_rect)

    def handle_click(self, pos):
        if self.game_over:
            print("Game is over!")
            self.calculate_final_scores()
            return None

        print(f"Current player now: {self.current_player}")

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
                # Check early terminate
                if self.early_termination():
                    self.game_over = True
                    self.calculate_final_scores()
                    return False
                else:
                    print(f"Board state after: {self.board[row][col]}")
            else:
                print(f"Move failed - tile already occupied")
                return None
        else:
            print(f"Click outside board bounds")

        return None

    def choose_heuristic(self):
        heuristic_choice = int(input("Choose heuristic (0=Simple, 1=Second, 2=Third): "))

        if heuristic_choice == 0:
            print(f"Simple heuristic value {simple_heuristic(self.board)}")
        elif heuristic_choice == 1:
            print(f"Middle heuristic value {self.second_heuristic()}")
        elif heuristic_choice == 2:
            print(f"Advanced heuristic value {self.third_heuristic()}")

        return heuristic_choice

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

            # self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def second_heuristic(self):
        heuristic = []

        # Save COMPLETE current state
        original_board = [row[:] for row in self.board]
        original_player1_moves = self.player1_moves[:]
        original_player2_moves = self.player2_moves[:]
        original_player1_valid_moves = self.player1_valid_moves.copy()
        original_player2_valid_moves = self.player2_valid_moves.copy()
        original_current_player = self.current_player
        original_last_move = self.last_move
        copy_valid_moves = list(self.player1_valid_moves).copy()

        for move in copy_valid_moves:
            current_move = move
            # Ensure we're evaluating Player 1 moves
            self.current_player = 1

            trial = self.make_move(*current_move)
            if trial:
                # Calculate heuristic using NEW state (after move)
                player1_pieces = len(self.player1_moves)  # ← Use self, not copy
                player2_pieces = len(self.player2_moves)  # ← Use self, not copy
                player1_moves_count = len(self.player1_valid_moves)  # ← Use self, not copy
                player2_moves_count = len(self.player2_valid_moves)  #

                heuristic_value = player1_pieces + player1_moves_count - player2_pieces - player2_moves_count
                print(f"Copy move: {current_move} - Advanced Heuristic value: {heuristic_value}")
                heuristic.append(heuristic_value)

            # copy_valid_moves.remove(current_move)
            # RESTORE original state
            self.board = [row[:] for row in original_board]  # ← FIX: Deep copy
            self.player1_moves = original_player1_moves[:]  # ← FIX: Deep copy
            self.player2_moves = original_player2_moves[:]  # ← FIX: Deep copy
            self.player1_valid_moves = original_player1_valid_moves.copy()  # ← FIX: Deep copy
            self.player2_valid_moves = original_player2_valid_moves.copy()  # ← FIX: Deep copy
            self.current_player = original_current_player
            self.last_move = original_last_move

        return heuristic

    def third_heuristic(self):
        heuristic = []

        # Save COMPLETE current state
        original_board = [row[:] for row in self.board]
        original_player1_moves = self.player1_moves[:]
        original_player2_moves = self.player2_moves[:]
        original_player1_valid_moves = self.player1_valid_moves.copy()
        original_player2_valid_moves = self.player2_valid_moves.copy()
        original_current_player = self.current_player
        original_last_move = self.last_move
        copy_valid_moves = list(self.player1_valid_moves).copy()

        for move in copy_valid_moves:
            current_move = move
            # Ensure we're evaluating Player 1 moves
            self.current_player = 1

            trial = self.make_move(*current_move)
            if trial:
                # Calculate heuristic using NEW state (after move)
                player1_pieces = len(self.player1_moves)  # ← Use self, not copy
                player2_pieces = len(self.player2_moves)  # ← Use self, not copy
                player1_moves_count = len(self.player1_valid_moves)  # ← Use self, not copy
                player2_moves_count = len(self.player2_valid_moves)  #

                heuristic_value = (player1_pieces+ player1_moves_count - player2_pieces - player2_moves_count) - self.calculate_territory() - self.calculate_thread() + self.calculate_capture_potential()
                print(f"Copy move: {current_move} - Advanced Heuristic value: {heuristic_value}")
                heuristic.append(heuristic_value)

            # copy_valid_moves.remove(current_move)
            # RESTORE original state
            self.board = [row[:] for row in original_board]  # ← FIX: Deep copy
            self.player1_moves = original_player1_moves[:]  # ← FIX: Deep copy
            self.player2_moves = original_player2_moves[:]  # ← FIX: Deep copy
            self.player1_valid_moves = original_player1_valid_moves.copy()  # ← FIX: Deep copy
            self.player2_valid_moves = original_player2_valid_moves.copy()  # ← FIX: Deep copy
            self.current_player = original_current_player
            self.last_move = original_last_move

        return heuristic

    def get_position_weight(self, row, col):
        center_row, center_col = BOARD_SIZE//2, BOARD_SIZE//2
        #Get distance from the center
        distance_from_center = abs(center_col - col) + abs(center_row - row)
        return MAX_DISTANCE - distance_from_center + 1

    def calculate_territory(self):
        player1_territory = 0
        player2_territory = 0

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.current_player == 1:
                    weight = self.get_position_weight(row,col)
                    player1_territory += weight
                if self.current_player == 2:
                    weight = self.get_position_weight(row,col)
                    player2_territory += weight
        return player1_territory - player2_territory

    def calculate_thread(self):
          # Save COMPLETE current state
        original_board = [row[:] for row in self.board]
        original_player1_moves = self.player1_moves[:]
        original_player2_moves = self.player2_moves[:]
        original_player1_valid_moves = self.player1_valid_moves.copy()
        original_player2_valid_moves = self.player2_valid_moves.copy()
        original_current_player = self.current_player
        original_last_move = self.last_move
        copy_valid_moves = list(self.player1_valid_moves).copy()

        thread = 0
        #simulate capture
        for move in copy_valid_moves:
            if self.check_captures(*move) is not None:
                thread += 1
            copy_valid_moves.remove(move)
            # RESTORE original state
            self.board = [row[:] for row in original_board]  # ← FIX: Deep copy
            self.player1_moves = original_player1_moves[:]  # ← FIX: Deep copy
            self.player2_moves = original_player2_moves[:]  # ← FIX: Deep copy
            self.player1_valid_moves = original_player1_valid_moves.copy()  # ← FIX: Deep copy
            self.player2_valid_moves = original_player2_valid_moves.copy()  # ← FIX: Deep copy
            self.current_player = original_current_player
            self.last_move = original_last_move

        return thread

    def calculate_capture_potential(self):
        player2_tiles = len(self.player2_moves)

        # Save COMPLETE current state
        original_board = [row[:] for row in self.board]
        original_player1_moves = self.player1_moves[:]
        original_player2_moves = self.player2_moves[:]
        original_player1_valid_moves = self.player1_valid_moves.copy()
        original_player2_valid_moves = self.player2_valid_moves.copy()
        original_current_player = self.current_player
        original_last_move = self.last_move
        copy_valid_moves = list(self.player1_valid_moves).copy()

        capture_potential = []
        for move in copy_valid_moves:
            if self.make_move(*move) is not None:
                player2_tiles_after = len(self.player2_moves)
                capture_potential.append(player2_tiles - player2_tiles_after)
            copy_valid_moves.remove(move)
            # RESTORE original state
            self.board = [row[:] for row in original_board]  # ← FIX: Deep copy
            self.player1_moves = original_player1_moves[:]  # ← FIX: Deep copy
            self.player2_moves = original_player2_moves[:]  # ← FIX: Deep copy
            self.player1_valid_moves = original_player1_valid_moves.copy()  # ← FIX: Deep copy
            self.player2_valid_moves = original_player2_valid_moves.copy()  # ← FIX: Deep copy
            self.current_player = original_current_player
            self.last_move = original_last_move

        return max(capture_potential)

    def get_heuristic_value_for_tile(self, row, col):
        if self.board[row][col] is not None:
            return None

        current_valid_moves = self.get_current_valid_moves()
        if (row, col) not in current_valid_moves:
            return None

        # Save current state
        original_board = [row[:] for row in self.board]
        original_player1_moves = self.player1_moves[:]
        original_player2_moves = self.player2_moves[:]
        original_player1_valid_moves = self.player1_valid_moves.copy()
        original_player2_valid_moves = self.player2_valid_moves.copy()
        original_current_player = self.current_player
        original_last_move = self.last_move

        # Simulate the move
        temp_success = self.make_move(row, col)
        heuristic_value = None

        if temp_success:
            if self.heuristic_choice == 0:
                heuristic_value = simple_heuristic(self.board)
            elif self.heuristic_choice == 1:
                # Calculate middle heuristic for this specific move
                player1_pieces = len(self.player1_moves)
                player2_pieces = len(self.player2_moves)
                player1_moves_count = len(self.player1_valid_moves)
                player2_moves_count = len(self.player2_valid_moves)
                heuristic_value = player1_pieces + player1_moves_count - player2_pieces - player2_moves_count
            elif self.heuristic_choice == 2:
                # Calculate advanced heuristic for this specific move
                player1_pieces = len(self.player1_moves)
                player2_pieces = len(self.player2_moves)
                player1_moves_count = len(self.player1_valid_moves)
                player2_moves_count = len(self.player2_valid_moves)
                heuristic_value = (player1_pieces + player1_moves_count - player2_pieces - player2_moves_count) - self.calculate_territory() - self.calculate_thread() + self.calculate_capture_potential()

        # Restore original state
        self.board = original_board
        self.player1_moves = original_player1_moves
        self.player2_moves = original_player2_moves
        self.player1_valid_moves = original_player1_valid_moves
        self.player2_valid_moves = original_player2_valid_moves
        self.current_player = original_current_player
        self.last_move = original_last_move

        return heuristic_value

if __name__ == "__main__":
    # Get heuristic choice
    print("🎮 Welcome to Tile Capture Game! 🎮")

    game = GameWithHeuristic()
    game.run()




import time
import random

class MinimaxTreeSample:
    def __init__(self, depth=1):
        self.depth = depth
        self.nodes_evaluated = 0
        self.best_move = None

    def evaluate_position(self, position):
        """Evaluate a game position (placeholder)"""
        # Simulate evaluation time
        time.sleep(0.1)
        return random.randint(-100, 100)

    def get_possible_moves(self, position):
        """Get all possible moves from current position"""
        # Return sample moves
        return [f"Move_{i}" for i in range(3)]

    def minimax(self, position, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        """Minimax algorithm with alpha-beta pruning"""
        max_eval = -1
        best_move = "Same move"
        return max_eval, best_move

    def run(self, game_view):
        """Run minimax computation and notify game view when complete"""
        print("Starting minimax computation...")

        self.nodes_evaluated = 0
        start_time = time.time()

        # Run minimax algorithm
        score, best_move = self.minimax("initial_position", self.depth, True)

        end_time = time.time()
        computation_time = end_time - start_time

        result = {best_move}

        print(f"Minimax completed: {result}")

        # Notify game view that computation is complete
        game_view.on_minimax_complete(result)
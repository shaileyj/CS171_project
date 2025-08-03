import pygame

# define constants that are used in many places so that we can
# edit them if we need to
BOARD_SIZE = 5

#these will be helpful for using an array to represent the board
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2

class GameTree:
    def __init__(self, value, board, left=None, right=None):
        self.value = value
        self.board = board
        self.left = left
        self.right = right

def simple_heuristic():
    pass

def advanced_heuristic():
    pass

def visualize_board(board):
    """Visualizes the game board"""
    pass

def visualize_game_tree(root):
    """Takes in a game tree and visualizes it (show value of each node)"""
    pass

def generate_moves(board, player):
    """Takes in a board state and returns all possible boards
    that can be yielded by player making one move"""
    pass

def build_tree(board, depth, heuristic):
    """Builds the minimax tree"""
    pass

def minimax(tree):
    """Runs the minimax algorithm"""
    pass

def main():
    state = ...
    tree = build_tree(state, 3)
    minimax(tree)
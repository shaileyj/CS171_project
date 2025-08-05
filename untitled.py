import pygame
import random

# define constants that are used in many places so that we can
# edit them if we need to
BOARD_SIZE = 5

#these will be helpful for using an array to represent the board
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2

class GameTree:
    def __init__(self, value, board, children=None):
        self.value = value
        self.board = board
        self.children = []

def simple_heuristic(board):
    pass

def advanced_heuristic(board):
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
    return []

def build_tree(board, depth, heuristic="simple", player=PLAYER_1):
    """Builds the minimax tree"""
    #I'm going to assume player 1 is the max player and
    #player 2 is the min player for simplicity
    if player == 1:
        #max nodes are initialized to a very small number
        root = GameTree(-1000000, board)
    else:
        #min nodes are initialized to a very large number
        root = GameTree(1000000, board)

    if depth <= 1:
        # leaf nodes are initialized to heuristic(board)
        if heuristic == "simple":
            root.value = simple_heuristic(board)
        else:
            root.value = advanced_heuristic(board)
        return root

    other = PLAYER_2 if player == PLAYER_1 else PLAYER_1
    #recursively generate subtree for each child node (each possible move
    #current player can take)
    for move in generate_moves(board, player):
        root.children.append(build_tree(move, depth-1, heuristic, other))
    return root


def minimax(tree, max_depth):
    """Runs the minimax algorithm"""
    pass

def main():
    state = ...
    tree = build_tree(state, 2, "simple")
    #minimax(tree)


if __name__ == "__main__":
    main()
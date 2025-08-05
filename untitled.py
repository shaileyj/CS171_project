import time
import pygame
import random

# define constants that are used in many places so that we can
# edit them if we need to
BOARD_SIZE = 5

#these will be helpful for using an array to represent the board
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

def visualize_game_tree(surface, root, start_x, start_y):
    """Takes in a game tree and visualizes it (show value of each node)"""
    border = pygame.draw.circle(surface, BLACK, (300, 300), 20)
    circle = pygame.draw.circle(surface, WHITE, (300, 300), 18)
    arial = pygame.font.SysFont("Arial", 18)
    text_surface = arial.render("11", False, BLACK)
    surface.blit(text_surface, (290, 290))


def generate_moves(board, player):
    """Takes in a board state and returns all possible boards
    that can be yielded by player making one move"""
    pass

def build_tree(board, depth, heuristic="simple", player=PLAYER_1):
    """Builds the minimax tree"""
    #I'm going to assume player 1 is the max player and
    #player 2 is the min player for simplicity

    root = GameTree(None, board)
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

def minimax(tree, is_max):
    """Runs the minimax algorithm"""
    #Base case: leaf nodes already store their value
    if len(tree.children) == 0:
        return tree.value
    #max layer finds max of its children recursively
    if is_max:
        tree.value = max(minimax(child, not is_max) for child in tree.children)
    #min layer finds min of its children recursively
    else:
        tree.value = min(minimax(child, not is_max) for child in tree.children)
    return tree.value

def main():
    pygame.font.init()
    surface = pygame.display.set_mode() #initializes a window


    surface.fill(WHITE) #sets background color to white

    pygame.display.flip() #displays the window

    #run loop, ends program when user closes window
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        visualize_game_tree(surface, None, 0, 0)
        pygame.display.flip() #update visual changes to display
    pygame.display.quit()


    #state = 0
    #tree = build_tree(state, 3, "simple")
    #print("minimax results:")
    #print(minimax(tree, True))


if __name__ == "__main__":
    main()
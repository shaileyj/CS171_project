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

#tree visualization
TREE_Y_DIST = 64
TREE_X_DIST = 128

class GameTree:
    def __init__(self, value, board, children=None):
        self.value = value
        self.board = board
        self.children = []
        self.color = WHITE

def simple_heuristic(board):
    pass

def advanced_heuristic(board):
    pass

def visualize_board(board):
    """Visualizes the game board"""
    pass

def visualize_node(surface, font, text, color, x, y):
    border = pygame.draw.circle(surface, BLACK, (x, y), 20)
    circle = pygame.draw.circle(surface, color, (x, y), 18)
    if text != None:
        text_surface = font.render(str(text), False, BLACK)
        surface.blit(text_surface, (x-10, y-10))

def visualize_game_tree(surface, root, start_x, start_y, x_dist, y_dist):
    """Takes in a game tree and visualizes it (show value of each node)"""
    arial = pygame.font.SysFont("Arial", 18)
    visualize_node(surface, arial, root.value, root.color, start_x, start_y)
    for i, child in enumerate(root.children):
        x = (start_x - (x_dist//2)) + i * ((x_dist * 2)/len(root.children))
        y = start_y + y_dist
        pygame.draw.line(surface, BLACK, (start_x, start_y+20), (x, y-10))
        visualize_game_tree(surface, child, x, y, x_dist//len(root.children), y_dist)

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
        print(root.value)
        return root

    other = PLAYER_2 if player == PLAYER_1 else PLAYER_1
    #recursively generate subtree for each child node (each possible move
    #current player can take)
    for move in generate_moves(board, player):
        root.children.append(build_tree(move, depth-1, heuristic, other))
    print(root.value)
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

    tree = build_tree(None, 4, "simple")
    tree.color = (255, 0, 0)
    print(minimax(tree, True))
    surface.fill(WHITE) #sets background color to white
    visualize_game_tree(surface, tree, 800, 200, 2**9, 2**6)

    pygame.display.flip() #displays the window

    #run loop, ends program when user closes window
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip() #update visual changes to display
    pygame.display.quit()


    #state = 0

    print("minimax results:")



if __name__ == "__main__":
    main()
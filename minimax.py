import time
import pygame
import random

WINDOW_SIZE = 800
BOARD_SIZE = 5
TILE_SIZE = 100 #WINDOW_SIZE / (BOARD_SIZE + 2)
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
WIP = (255, 209, 248)
CURR = (255, 110, 139)
FIN = (156, 156, 156)


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
    return random.randint(1, 20)

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
    return [1, 2, 3]

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

def ai_move(board, player, depth, heuristic):
    tree = build_tree(board, depth, heuristic, player)
    is_max = (player == PLAYER_1)
    value = minimax(tree, is_max)
    for child in tree.children:
        if value == child.value:
            return child.board


def one_step_minimax(tree, is_max, parent):
    #base case updates parent node
    if tree.value is not None and parent is not None:
        if parent.value is None:
            parent.value = tree.value
        elif is_max:
            parent.value = min(parent.value, tree.value)
        else:
            parent.value = max(parent.value, tree.value)
        return [] #no recursive calls spawned
    elif tree.value is not None:
        return []
    #max layer finds max of its children recursively
    if is_max:
        return [(child, not is_max, tree) for child in tree.children]
    #min layer finds min of its children recursively
    else:
        return [(child, not is_max, tree) for child in tree.children]

def show_minimax_step_and_update_stack(stack, prev, prev_par):
    args = stack.pop()
    return_args = one_step_minimax(*args)
    if return_args:
        stack.append(args)
    if prev:
        prev.color = WIP
    if prev_par and args[2] and args[2] != prev_par:
        prev_par.color = WIP
    if args[2]:
        args[2].color = CURR
    args[0].color = CURR
    stack.extend(return_args)
    prev = args[0]
    prev_par = args[2]
    return prev, prev_par

def display_layer_labels(surface, annotation_font):
    start = 190
    gap = 2 ** 6
    for i in range(4):
        if i % 2 == 0:
            text = "MAX"
        else:
            text = "MIN"
        text_surface = annotation_font.render(text, False, BLACK)
        surface.blit(text_surface, (150, start + gap * i))

def draw_board(screen, board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = BOARD_OFFSET + col * TILE_SIZE
            y = BOARD_OFFSET + row * TILE_SIZE

            if board[row][col] is None:
                # if (row,col) in self.valid_move:
                #     return LIGHT_GRAY
                # else:
                color = WHITE
            elif board[row][col] == 1:
                color = RED
            else:
                color = BLUE
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
            # pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, BOARD_SIZE),2)

            # if (row, col) in self.valid_move:
            #     center_x = x + TILE_SIZE//2
            #     center_y = y + TILE_SIZE//2
            #     pygame.draw.circle(self.screen, GREEN, (center_x, center_y), TILE_SIZE//2)
    # grid
    for col in range(BOARD_SIZE + 1):  # vertical
        x = BOARD_OFFSET + col * TILE_SIZE
        pygame.draw.line(screen, BLACK, (x, BOARD_OFFSET), (x, BOARD_OFFSET + BOARD_SIZE * TILE_SIZE), 2)
    for row in range(BOARD_SIZE + 1):  # horizontal
        y = BOARD_OFFSET + row * TILE_SIZE
        pygame.draw.line(screen, BLACK, (BOARD_OFFSET, y), (BOARD_OFFSET + BOARD_SIZE * TILE_SIZE, y), 2)

def main():
    pygame.font.init()
    surface = pygame.display.set_mode() #initializes a window
    annotation_font = pygame.font.SysFont("Arial", 24)
    surface.fill(WHITE)  # sets background color to white

    tree = build_tree(None, 4, "simple")
    tree.color = CURR

    #initialize variables
    stack = [(tree, True, None), ]
    prev = None
    prev_par = None
    running = True
    annotations = []
    for i in range(100):
        annotations.append(None)
    annotations[0] = "this is a minimax tree"
    counter = 0

    #display initial values
    text_surface = annotation_font.render(str("Press ->, D, or space to move forward"), False, BLACK)
    surface.blit(text_surface, (100, 450))
    pygame.display.flip()

    #run loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT)\
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_d)\
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                surface.fill(WHITE)
                if not stack:
                    running = False
                    continue
                prev, prev_par = show_minimax_step_and_update_stack(stack, prev, prev_par)
                visualize_game_tree(surface, tree, 600, 200, 2**9, 2**6)
                draw_board(surface, prev.board)
                draw_board(surface, prev_par.board)
                if annotations[counter] is not None:
                    text_surface = annotation_font.render(str(annotations[counter]), False, BLACK)
                    surface.blit(text_surface, (100, 450))
                display_layer_labels(surface, annotation_font)
                pygame.display.flip() #update visual changes to display
                counter += 1

    pygame.display.quit()
    #state = 0

    print("minimax results:")

if __name__ == "__main__":
    main()
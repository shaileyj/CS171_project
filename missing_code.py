from minimax import generate_moves, simple_heuristic

PLAYER_1 = 1
PLAYER_2 = 2

class GameTree:
    def __init__(self, value, board, children=None):
        self.value = value
        self.board = board
        self.children = []

def build_tree(board, depth, player=PLAYER_1):
    """Builds the minimax tree"""
    #Assume player 1 is the max player and
    #player 2 is the min player for simplicity

    root = GameTree(None, board)
    children = generate_moves(board, player)
    if depth <=1 or len(children) == 0:
        # leaf nodes are initialized to heuristic(board)
        # fill out here

    other = PLAYER_2 if player == PLAYER_1 else PLAYER_1
    for move in children:
        # fill out here

    return root

def minimax(tree, is_max):
    """Runs the minimax algorithm"""
    """Using simple heuristic"""
    #Base case:
    if len(tree.children) == 0:
        tree.value = simple_heuristic(tree.board)
        # fill out here

    #Recursive cases:
    if is_max:
        # fill out here

    else:
        # fill out here


    return tree.value




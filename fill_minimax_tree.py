import pygame
import minimax

YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

def manage_stack(stack):
    if not stack:
        return
    item = stack[-1]
    if item.value is not None:
        item = stack.pop()
    while item.value is None and any(child.value is None for child in item.children):
        stack.extend(reversed(item.children))
        item = stack[-1]
    print([node.value for node in stack])
    item.color = YELLOW
    if stack and stack[-1] == item:
        stack.pop()
    return item

def one_step(tree):
    if tree is None or tree.children is None:
        return []
    else:
        return reversed(tree.children)

def get_next_node(stack):
    curr = stack.pop()
    curr.color = YELLOW
    next_nodes = one_step(curr)
    while next_nodes[0].value is None:
        stack.extend(next_nodes)
        next_nodes = one_step(curr)
    stack.extend(next_nodes)
    return curr

def main(surface):
    board = [
        [1, 1, 1, 2, None],
        [1, 1, 1, 2, 2],
        [1, 1, 1, None, 2],
        [1, None, 1, 2, 2],
        [1, None, None, 2, 2]
    ]
    tree = minimax.build_tree(board, 4, "simple")
    font = pygame.font.SysFont("arial", 24)
    running = True
    user_input = ""
    stack = [tree, tree] #keeps track of node to "process"
    curr = manage_stack(stack)
    prev = curr
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key != pygame.K_RETURN:
                    user_input += event.unicode
                elif stack:
                    curr.value = user_input
                    prev = curr
                    prev.color = WHITE
                    curr = manage_stack(stack)
                    user_input = ""


        surface.fill(minimax.WHITE)
        temp = "Your Input: " + user_input
        text_surface = font.render(temp, False, minimax.BLACK)
        surface.blit(text_surface, (150, 100))
        minimax.visualize_game_tree(surface, tree, 600, 200, 2**9, 2**6)
        minimax.display_layer_labels(surface, font)
        pygame.display.flip() #update visual changes to display

pygame.init()
surface = pygame.display.set_mode()  # initializes a window
surface.fill(minimax.WHITE)
main(surface)

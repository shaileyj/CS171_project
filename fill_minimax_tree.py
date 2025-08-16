import pygame
import minimax

YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

def manage_stack(stack, answer_stack):
    if not stack:
        return
    item = stack[-1]
    a_item = answer_stack[-1]
    if item.value is not None:
        item = stack.pop()
        a_item = answer_stack.pop()
    while item.value is None and any(child.value is None for child in item.children):
        stack.extend(reversed(item.children))
        answer_stack.extend(reversed(a_item.children))
        item = stack[-1]
        a_item = answer_stack[-1]
    print([node.value for node in stack])
    item.color = YELLOW
    if stack and stack[-1] == item:
        stack.pop()
        answer_stack.pop()
    return item, a_item

def main(surface):
    board = [
        [1, 1, 1, 2, None],
        [1, 1, 1, 2, 2],
        [1, 1, 1, None, 2],
        [1, None, 1, 2, 2],
        [1, None, None, 2, 2]
    ]
    tree = minimax.build_tree(board, 4, "simple")
    answer_key = minimax.build_tree(board, 4, "simple")
    minimax.minimax(answer_key, True)
    font = pygame.font.SysFont("arial", 24)
    running = True
    user_input = ""

    stack = [tree, tree] #keeps track of node to "process"
    answer_stack = [answer_key, answer_key]
    curr, curr_ans = manage_stack(stack, answer_stack)
    prev, prev_ans = curr, curr_ans

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
                    prev_ans = curr_ans
                    if int(prev.value) == int(prev_ans.value):
                        print(prev.value, prev_ans.value, "green")
                        prev.color = GREEN
                        if len(stack) > 1:
                            curr, curr_ans = manage_stack(stack, answer_stack)
                        user_input = ""
                    else:
                        print(prev.value, prev_ans.value, "red")
                        prev.color = RED
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

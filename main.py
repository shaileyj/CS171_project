#Team Members: Shailey Joseph, My Nguyen
import sys
import time
import pygame
import minimax
import TileCaptureGame

WHITE = (255, 255, 255)

def main():
    pygame.font.init()
    surface = pygame.display.set_mode()  # initializes a window
    surface.fill(WHITE)  # sets background color to white

    game = TileCaptureGame.TileCaptureGame(surface)
    game.run()
    surface.fill(WHITE)


    board = [
        [1, 1, 1, 2, None],
        [1, 1, 1, 2, 2],
        [1, 1, 1, 2, 2],
        [1, 1, 1, 2, 2],
        [1, None, None, 2, 2]
    ]

    alt_board = [
        [1, 1, 1, 2, None],
        [1, None, 2, 2, 2],
        [1, None, 2, 2, 2],
        [1, None, None, 2, 2],
        [1, 1, 2, 2, 2]]

    #(optional) write some code to display the game rules
    minimax.main(surface, alt_board)
    #game = TileCaptureGame.TileCaptureGame(board)
    #game.run()
    #
    # running = True
    # while running:
    #     game.draw_board()
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #
    #     time.sleep(2)
    #     move = game.player1_valid_moves.pop()
    #     game.player1_valid_moves.add(move)
    #     game.make_move(*move)
    #     time.sleep(2)
    #     move = game.player2_valid_moves.pop()
    #     game.player2_valid_moves.add(move)
    #     game.make_move(*move)
    #
    #
    #
    #
    #     # game.draw_board()
    #     pygame.display.flip()
    #     game.clock.tick(60)

    
    pygame.quit()
    sys.exit()

main()

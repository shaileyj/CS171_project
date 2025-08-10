import sys
import time
import pygame
import GameStateSlide
import GameStateView
import minimax
import TileCaptureGame

def main():

    board = [
        [1, 1, 1, 2, None],
        [1, 1, 1, 2, 2],
        [1, 1, 1, 2, 2],
        [1, 1, 1, 2, 2],
        [1, None, None, 2, 2]
    ]
    #(optional) write some code to display the game rules
    minimax.main(board)
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

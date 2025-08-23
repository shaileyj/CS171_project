import unittest
import Part3
import minimax

class UserMinimaxTest(unittest.TestCase):
    def test_1(self):
        board = [[1, 1, 1, None, None],
        [1, None, None, 2, 2],
        [1, None, 2, 2, 2],
        [1, None, None, 2, 2],
        [1, None, 2, 2, 2]]
        user_tree = minimax.build_tree(board, 4)
        minimax.minimax(user_tree, True)
        answer_tree = Part3.build_tree(board, 4)
        Part3.minimax(answer_tree, True)
        self.assertTrue(minimax.compare_tree(user_tree, answer_tree), "FAILED: Basic test " )

    def test_2(self): #board empty
        board = [[None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None]]
        user_tree = minimax.build_tree(board, 4)
        minimax.minimax(user_tree, True)
        answer_tree = Part3.build_tree(board, 4)
        Part3.minimax(answer_tree, True)
        self.assertTrue(minimax.compare_tree(user_tree, answer_tree),  "FAILED: Empty board test ")

    def test_3(self): #player 1 dominance
        board = [[1, 1, 1, 1, 1],
                 [1, 1, 1, 1, None],
                 [1, 1, 1, None, None],
                 [1, 1, None, None, None],
                 [1, None, None, None, None]]
        user_tree = minimax.build_tree(board, 3)
        minimax.minimax(user_tree, True)
        answer_tree = Part3.build_tree(board, 3)
        Part3.minimax(answer_tree, True)
        self.assertTrue(minimax.compare_tree(user_tree, answer_tree), "FAILED: Single player dominance test ")

    def test_4(self): #Nearly Full
        board = [[1, 2, 1, 1, 1],
                 [1, 2, 1, 1, None],
                 [1, 1, 1, 1, None],
                 [2, 2, 2, 2, 2],
                 [1, 1, 1, 1, 1]]
        user_tree = minimax.build_tree(board, 3)
        minimax.minimax(user_tree, True)
        answer_tree = Part3.build_tree(board, 3)
        Part3.minimax(answer_tree, True)
        self.assertTrue(minimax.compare_tree(user_tree, answer_tree), "FAILED: Nearly full board test ")

    def test_5(self): #Depth 0
        board = [[1, 2, 1, 1, 1],
                 [1, 2, 1, 1, 2],
                 [1, 1, 1, 1, 2],
                 [2, 2, 2, 2, 2],
                 [1, 1, 1, 1, 1]]
        user_tree = minimax.build_tree(board, 0)
        minimax.minimax(user_tree, True)
        answer_tree = Part3.build_tree(board, 0)
        Part3.minimax(answer_tree, True)
        self.assertTrue(minimax.compare_tree(user_tree, answer_tree), "FAILED: Terminal test ")



if __name__ == '__main__':
    unittest.main()

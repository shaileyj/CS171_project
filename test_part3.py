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
        minimax.minimax(board, True)
        answer_tree = Part3.build_tree(board, 4)
        Part3.minimax(board, True)
        self.assertTrue(minimax.compare_tree(user_tree, answer_tree))


if __name__ == '__main__':
    unittest.main()

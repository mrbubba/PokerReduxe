import unittest
from myhand.mask import add_board, board_list, get_board


class TestMaskGeneration(unittest.TestCase):

    def test_board_generator(self):
        """
        Can we generate boards?
        """
        expected = ["14s","14h","14d"]
        expected.sort()
        board = get_board()
        actual = next(board)
        actual.sort()
        self.assertListEqual(expected, actual)

    def test_add_board(self):
        """
        can we add a board too our master list of boards?
        """
        expected = ["14s", "14h", "14d"]
        expected.sort()
        add_board(expected)
        self.assertIn(expected, board_list['flop'])

    def test_add_board_only_once(self):
        """
        can we ensure there are no duplicates when we add a board?
        """

        expected = ["14s", "14h", "14d"]
        expected.sort()
        add_board(expected)
        add_board(expected)
        self.assertEqual(board_list['flop'].count(expected), 1)
    
    def test_add_board_limits_size(self):
        """
        Do we raise a value error if we pass the wrong length board?
        """
        test_value = [1,2,3,4,5,6]
        with self.assertRaises(ValueError):
            add_board(test_value)

    def test_add_board_lengths(self):
        """
        Do we add our boards to the correct sublist of board_list?
        """
        flop = ["14s", "14h", "14d"]
        turn = ["14s", "14h", "14d", "14c"]
        river = ["14s", "14h", "14d", "14c", "13s"]
        add_board(flop)
        add_board(turn)
        add_board(river)

        self.assertIn(flop, board_list['flop'])
        self.assertEqual(len(board_list['flop']), 1)
        self.assertIn(turn, board_list['turn'])
        self.assertEqual(len(board_list['turn']), 1)
        self.assertIn(river, board_list['river'])
        self.assertEqual(len(board_list['river']), 1)

if __name__ == '__main__':
    unittest.main()
from unittest import TestCase
from domain.boardJSON import BoardJSON
from validator.boardValidator import validate_column, InvalidColumn


class Test(TestCase):
    def test_validate_column(self):
        board = BoardJSON()
        ans = validate_column(board, 1)
        self.assertEqual(ans, True)

        board.drop_piece(board, 0, 0, 1)
        board.drop_piece(board, 1, 0, 1)
        board.drop_piece(board, 2, 0, 1)
        board.drop_piece(board, 3, 0, 1)
        board.drop_piece(board, 4, 0, 1)
        board.drop_piece(board, 5, 0, 1)

        self.assertRaises(InvalidColumn, validate_column, board, 0)
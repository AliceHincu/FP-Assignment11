from unittest import TestCase
from domain.boardJSON import BoardJSON


class TestBoardJSON(TestCase):
    def test_winning(self):
        board = BoardJSON()
        board.create_board()

        board.drop_piece(board, 0, 1, 1)
        board.drop_piece(board, 0, 2, 1)
        board.drop_piece(board, 0, 3, 1)
        board.drop_piece(board, 0, 4, 1)
        win = board.winning(board, 1)
        self.assertEqual(win, True)

        board.create_board()
        board.drop_piece(board, 1, 0, 1)
        board.drop_piece(board, 2, 0, 1)
        board.drop_piece(board, 3, 0, 1)
        board.drop_piece(board, 4, 0, 1)
        win = board.winning(board, 1)
        self.assertEqual(win, True)

        board.create_board()
        board.drop_piece(board, 1, 1, 1)
        board.drop_piece(board, 2, 2, 1)
        board.drop_piece(board, 3, 3, 1)
        board.drop_piece(board, 4, 4, 1)
        win = board.winning(board, 1)
        self.assertEqual(win, True)

        board.create_board()
        board.drop_piece(board, 4, 1, 1)
        board.drop_piece(board, 3, 2, 1)
        board.drop_piece(board, 2, 3, 1)
        board.drop_piece(board, 1, 4, 1)
        win = board.winning(board, 1)
        self.assertEqual(win, True)


    def test_save(self):
        pass

    def test__load(self):
        pass

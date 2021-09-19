from unittest import TestCase
from validator.playerValidator import validate_mode, InvalidInputMode
from domain.boardJSON import BoardJSON
from validator.playerValidator import validate_input, InvalidInput


class Test(TestCase):
    def test_validate_input(self):
        board = BoardJSON()
        self.assertRaises(InvalidInput, validate_input, board, "33")
        self.assertRaises(InvalidInput, validate_input, board, "casvcas")

        col = validate_input(board, "4")
        self.assertEqual(col, 4)

    def test_validate_mode(self):
        board = BoardJSON()
        self.assertRaises(InvalidInputMode, validate_mode, "4", "game_mode")
        self.assertRaises(InvalidInputMode, validate_mode, "4", "difficulty_mode")

        op = validate_mode("2", "game_mode")
        op2 = validate_mode("2", "difficulty_mode")

        self.assertEqual(op, 2)
        self.assertEqual(op2, 2)



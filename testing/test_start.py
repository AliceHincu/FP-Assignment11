from unittest import TestCase
from start_game.start import Game
from domain.boardJSON import BoardJSON


class TestGame(TestCase):

    def test_next_turn(self):
        game = Game()

        game.set_battle_mode("player vs player")
        turn = 'player1'
        actual_turn = game.next_turn(turn)
        expected_turn = 'player2'
        self.assertEqual(actual_turn, expected_turn)

        turn = 'player2'
        actual_turn = game.next_turn(turn)
        expected_turn = 'player1'
        self.assertEqual(actual_turn, expected_turn)

        game.set_battle_mode("player vs computer")
        turn = 'player1'
        actual_turn = game.next_turn(turn)
        expected_turn = 'player_ai'
        self.assertEqual(actual_turn, expected_turn)

        turn = 'player_ai'
        actual_turn = game.next_turn(turn)
        expected_turn = 'player1'
        self.assertEqual(actual_turn, expected_turn)

    def test_play_turn(self):
        game = Game()
        board = BoardJSON()
        board.create_board("player1", "player vs player")
        game_over, board, turn = game.play_turn(board, "player1", 4, 1)
        import numpy as np
        actual_matrix = np.flip(board.boardmatrix(), 0)
        matrix = np.zeros((6, 7))
        matrix[0][4] = 1
        expected_matrix = np.flip(matrix, 0)
        self.assertEqual(expected_matrix.tolist(), actual_matrix.tolist())

        game_over, board, turn = game.play_turn(board, "player1", 4, 1)
        game_over, board, turn = game.play_turn(board, "player1", 4, 1)
        game_over, board, turn = game.play_turn(board, "player1", 4, 1)

        self.assertEqual(game_over, True)

    def test_run_game(self):
        game = Game()
        board = BoardJSON()
        game_over, board, turn = game.run_game(board, "player1", 3)
        game_over, board, turn = game.run_game(board, "player2", 3)
        game_over, board, turn = game.run_game(board, "player_ai", 3)

        self.assertEqual(game_over, False)

        board, turn = game.new_game()
        import numpy as np
        matrix = np.zeros((6, 7))
        expected_matrix = np.flip(matrix, 0)
        self.assertEqual(board.boardmatrix().tolist(), expected_matrix.tolist())
        game_over, board, turn = game.play_turn(board, "player1", 4, 1)

        board, turn, battle_mode = game.load_game()
        expected_matrix[0][4] = 1
        self.assertEqual(expected_matrix.tolist(), board.boardmatrix().tolist())



# ----- IMPORT ZONE -----
import json
import os
import numpy as np


# ----- EXCEPTIONS ZONE -----
class InvalidJSON(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# ----- CLASS ZONE -----
class BoardJSON:
    def __init__(self):
        self._BOARD = None
        self._ROWCOUNT = 6
        self._COLUMNCOUNT = 7
        self._DIMENSION = (self._ROWCOUNT, self._COLUMNCOUNT)
        self._turn = None
        self._battle_mode = None
        self._difficulty = None
        self._file_path = 'C:\\Users\\Sakura\\Documents\\GitHub\\FP\\a11-913AliceHincu\\start_game\\Board.json'
        self._turn_path = 'C:\\Users\\Sakura\\Documents\\GitHub\\FP\\a11-913AliceHincu\\start_game\\Turn.json'
        self._battle_mode_path = 'C:\\Users\\Sakura\\Documents\\GitHub\\FP\\a11-913AliceHincu\\start_game\\' \
                                 'Battle mode.json'
        self._difficulty_path = 'C:\\Users\\Sakura\\Documents\\GitHub\\FP\\a11-913AliceHincu\\start_game\\' \
                                'Difficulty.json'
        self._load()

    # ----- CREATE & STORE -----
    def create_board(self, turn='player1', battle_mode='player vs player'):
        """
        --- Description
        Create a new empty board

        --- Parameters
        :param turn: the turn is set to player1 (type: <str>)
        :param battle_mode: the battle_mode is set to player vs player (type: <str>)
        """
        self._BOARD = np.zeros(self.dimension())
        self.save(turn, battle_mode, self._difficulty)

    def store_board(self, matrix, turn, battle_mode, difficulty):
        """
        --- Description
        Store the board

        --- Parameters
        :param matrix: the matrix of the board (type: <list of lists>)
        :param turn: remember whose turn it is, player1 or player2 (type: <str>)
        :param battle_mode: player vs player or player vs computer (type: <str>)
        :param difficulty: the difficulty in case the player plays with the computer, easy, medium or hard (type: <str>)
        """
        self._BOARD = matrix
        self.save(turn, battle_mode, difficulty)

    # ----- SETTERS -----
    def set_dif(self, dif):
        """
        Set the difficulty
        :param dif: easy, medium or hard (type: <str>)
        """
        self._difficulty = dif

    def set_battle_mode(self, bm):
        """
        Set the battle_mode
        :param bm: player vs player or computer vs player (type: <str>)
        """
        self._battle_mode = bm

    # ----- GETTERS -----
    def boardmatrix(self):
        """
        --- Return
        :return: the matrix of the board (type: <list of lists>)
        """
        return self._BOARD

    def rowcount(self):
        """
        --- Return
        :return: the number of rows (type: int)
        """
        return self._ROWCOUNT

    def columncount(self):
        """
        --- Return
        :return: the number of columns (type: int)
        """
        return self._COLUMNCOUNT

    def dimension(self):
        """
        --- Return
        :return: the dimension (type: <tuple>)
        """
        return self._DIMENSION

    def turn(self):
        """
        --- Return
        :return: whose turn it is (type: <str>)
        """
        return self._turn

    def battle_mode(self):
        """
        --- Return
        :return: player bs player or player vs computer (type: <str>)
        """
        return self._battle_mode

    def difficulty(self):
        """
        --- Return
        :return: the difficulty, easy, medium or hard (type: <str>)
        """
        return self._difficulty

    def __getitem__(self, index):
        return self.boardmatrix()[index]

    @staticmethod
    def get_available_row(board, col):
        """
        On what row does the piece drop
        -- Variables:
        :param board: the board itself (type: class <Board>)
        :param col: the column input from the player (type: <int>)

        :return: the row (type: <int>)
        """
        matrix = board.boardmatrix()
        for row in range(board.rowcount()):
            if matrix[row][col] == 0:
                return row

    @staticmethod
    def drop_piece(board, row, col, piece):
        """
        Drops the piece where it should go
        -- Variables:
        :param board: the board itself (type: class <Board>)
        :param col: the column input from the player (type: <int>)
        :param row: the row (type:<int>)
        :param piece: the piece (type:<int>)
        """
        matrix = board.boardmatrix()
        matrix[row][col] = piece

    @staticmethod
    def winning(board, piece):
        """
        Check if winning
        -- Variables:
        :param board: the board itself (type: class <Board>)
        :param piece: the piece (type:<int>)

        :return: if the player is winning or not (type: <bool>)
        """
        expected_list = [piece] * 4

        # Score Horizontal
        for r in range(board.rowcount()):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(board.columncount() - 3):
                mini_row_list = row_array[c:(c + 4)]
                if mini_row_list == expected_list:
                    return True

        # Score Vertical
        for c in range(board.columncount()):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(board.rowcount() - 3):
                mini_col_list = col_array[r:(r + 4)]
                if mini_col_list == expected_list:
                    return True

        # Score Diagonal (low left, rise to right)
        for r in range(board.rowcount() - 3):
            for c in range(board.columncount() - 3):
                mini_diag_list = [board[r + i][c + i] for i in range(4)]
                if mini_diag_list == expected_list:
                    return True

        # Score Diagonal (up left, go down to right)
        for r in range(board.rowcount() - 3):
            for c in range(board.columncount() - 3):
                mini_diag_list = [board[r + 3 - i][c + i] for i in range(4)]
                if mini_diag_list == expected_list:
                    return True

        return False

    def save(self, turn, battle_mode, difficulty):
        """
        --- Description
        Save the file

        --- Parameters
        :param turn: (type: <str>)
        :param battle_mode: (type: <str>)
        :param difficulty: (type: <str>)
        """
        board = {}
        matrix = self.boardmatrix()
        for i in range(self.rowcount()):
            row = {}
            for j in range(self.columncount()):
                row[j] = str(matrix[i][j])
            board[i] = row
        with open(os.path.join(self._file_path, ), 'w') as f:
            json.dump(board, f)
        with open(os.path.join(self._turn_path, ), 'w') as f:
            json.dump(turn, f)
        with open(os.path.join(self._battle_mode_path, ), 'w') as f:
            json.dump(battle_mode, f)
        with open(os.path.join(self._difficulty_path, ), 'w') as f:
            json.dump(difficulty, f)
        self._turn = turn
        self._battle_mode = battle_mode
        self._difficulty = difficulty
        f.close()

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """

        with open(self._file_path) as f:
            try:
                data = json.load(f)
            except InvalidJSON:
                f.close()
                return
        with open(self._turn_path) as f:
            try:
                turn = json.load(f)
            except InvalidJSON:
                f.close()
                return
        with open(self._battle_mode_path) as f:
            try:
                battle_mode = json.load(f)
            except InvalidJSON:
                f.close()
                return
        with open(self._difficulty_path) as f:
            try:
                difficulty = json.load(f)
            except InvalidJSON:
                f.close()
                return
        self.create_board(turn, battle_mode)
        self.set_dif(difficulty)
        matrix = self.boardmatrix()
        for row in data.keys():
            for col in data[row]:
                matrix[int(row)][int(col)] = data[row][col]
        self.store_board(matrix, turn, battle_mode, difficulty)
        f.close()

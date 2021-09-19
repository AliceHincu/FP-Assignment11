import math
from validator.boardValidator import validate_column, InvalidColumn
import random
import copy
from start_game.start import Game


class EasyMode:
    """
    --- Description
    Easy mode means:
        - the computer generates random values for the columns.
        - it does not take into consideration the player's moves.
    """

    @staticmethod
    def calculate_move(board):
        """
        --- Description
        Pick a random valid column

        --- Parameters
        :param board: (type: <class>)

        --- Return
        :return: the final column (type: <int>)
        """
        valid_columns = []
        for col in range(board.columncount()):
            try:
                _ok = validate_column(board, col)
                valid_columns.append(col)
            except InvalidColumn:
                pass
        final_col = int(random.choice(valid_columns))
        return final_col


class MediumMode(EasyMode, Game):
    """
    --- Description
    Medium mode means:
        - the computer evaluates what it's best for itself.
        - it does not take into consideration the player's moves (it doesn't attack).
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def evaluate_score(mini_list, piece, difficulty):
        """
        --- Description
        It adds to the score if the function finds a combination with pieces for the computer.
        It subtracts from the score if the function finds a combination with pieces for the player.(for hard mode)

        --- Parameters
        :param mini_list: the list of the four pieces (type: <list>)
        :param piece: the value of the piece. For computer the piece is 2 (type: <int>)
        :param difficulty: can be either medium or hard (type: <str>)

        --- Return
        :return: returns the final score (type: <int>)
        """
        score = 0
        opponent_piece = 1

        # Add to the score for computer
        if mini_list.count(piece) == 4:
            # we found 4 in a row
            score += 10000
        elif mini_list.count(piece) == 3 and mini_list.count(0) == 1:
            # we found 3 in a row (3 computer pieces and an empty slot)
            score += 5
        elif mini_list.count(piece) == 2 and mini_list.count(0) == 2:
            # we found 2 in a row (2 computer pieces and 2 empty slots)
            score += 2

        if difficulty == "hard":
            # Subtract from the score for the player
            if mini_list.count(opponent_piece) == 3 and mini_list.count(0) == 1:
                # we found 3 in a row (3 player pieces and an empty slot)
                score -= 400

        return score

    def score_position(self, board, piece, difficulty):
        """
        --- Description
        Calculates the score of the given board.

        --- Parameters
        :param board: (type: <class>)
        :param piece: the value of the piece. For computer the piece is 2 (type: <int>)
        :param difficulty: can be either medium or hard (type: <str>)

        --- Return
        :return: returns the score (type: <int>)
        """
        score = 0

        # Make the center column a priority since it gives a lot more chances to win
        center_array = [int(i) for i in list(board[:, self.columncount() // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(self._ROWCOUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(board.columncount() - 3):
                mini_row_list = row_array[c:(c + 4)]
                score += self.evaluate_score(mini_row_list, piece, difficulty)

        # Score Vertical
        for c in range(self._COLUMNCOUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(board.rowcount() - 3):
                mini_col_list = col_array[r:(r + 4)]
                score += self.evaluate_score(mini_col_list, piece, difficulty)

        # Score Diagonal (low left, rise to right)
        for r in range(self.rowcount() - 3):
            for c in range(self.columncount() - 3):
                mini_diag_list = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_score(mini_diag_list, piece, difficulty)

        # Score Diagonal (up left, go down to right)
        for r in range(self.rowcount() - 3):
            for c in range(self.columncount() - 3):
                mini_diag_list = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_score(mini_diag_list, piece, difficulty)

        return score

    def get_valid_locations(self, board):
        """
        --- Description
        Makes a list with all the valid locations where the piece can be dropped.
        If a column is full, it means it is not valid.

        --- Parameters
        :param board: (type: <class>)

        --- Return
        :return: the valid locations (type: <list>)
        """
        valid_locations = []
        for col in range(self._COLUMNCOUNT):
            try:
                if validate_column(board, col):
                    valid_locations.append(col)
            except InvalidColumn:
                pass
        return valid_locations

    def pick_best_move(self, board, piece):
        """
        --- Description
        Calculates the score for every possibility (nr_columns possibilities)
        Finds the best score associated with the best column and returns the column.

        --- Parameters
        :param board: (type: <class>)
        :param piece: the value of the piece. For computer the piece is 2 (type: <int>)

        --- Return
        :return: returns the best column (type: <int>)
        """
        valid_locations = self.get_valid_locations(board)
        best_score = -8000  # start with something very low so it doesn't mess up the "evaluate score" function
        best_column = random.choice(valid_locations)  # random column in case the scores are all equal

        for col in valid_locations:
            row = self.get_available_row(board, col)
            temp_board = copy.deepcopy(board)
            self.drop_piece(temp_board, row, col, piece)
            score = self.score_position(temp_board, piece, "medium")
            if score > best_score:
                best_score = score
                best_column = col

        return best_column


class HardMode(MediumMode):
    def __init__(self):
        super().__init__()
        self._player_piece = 1
        self._computer_piece = 2

    def is_terminal_node(self, board):
        """
        A terminal node is when:
            -the player wins
            -the computer wins
            -the board if full
        :param board: (type: <class)
        :return: true if it's terminal, false if it isn't (type: <bool>)
        """
        return self.winning(board, self._player_piece) or self.winning(board, self._computer_piece) or \
            len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        --- Description:
        Hard mode means:
        - the computer evaluates what it's best for itself.
        - it takes into consideration the player's moves (it attacks).

        Solving Connect 4 can been seen as finding the best path in a decision tree where each node is a Position.
        At each node player has to choose one move leading to one of the possible next positions.
        When it is the computer's turn, it'll want to choose the best possible move that will maximize its score.
        But next turn the opponent will try himself to maximize his score, thus minimizing the computer's.

        --- Parameters:
        :param board: (type: <class>)
        :param depth: how many branches deep into the algorithm (type: <int>)
        :param alpha:
        :param beta:
        :param maximizing_player: true for maximizing the computer, false for minimizing the player (type: <bool>)
        :return: the best column and the score
        """
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                # which case of the three conditions are respected
                if self.winning(board, self._computer_piece):
                    return None, 10000000  # very high score
                elif self.winning(board, self._player_piece):
                    return None, -10000000  # very low score
                else:
                    return None, 0  # Game is over, no more valid moves
            else:
                # Depth is zero => find the heuristic value of node
                return None, self.score_position(board, self._computer_piece, "hard")

        if maximizing_player:  # max the computer (take the bigger value)
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_available_row(board, col)
                board_copy = copy.deepcopy(board)
                self.drop_piece(board_copy, row, col, self._computer_piece)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                # alpha = max(value, alpha)
                # if alpha >= beta:
                #     break
            return column, value
        else:  # minimizing player (take the lowest value)
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_available_row(board, col)
                board_copy = copy.deepcopy(board)
                self.drop_piece(board_copy, row, col, self._player_piece)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                    # beta = min(value, beta)
                    # if alpha >= beta:
                    #     break
            return column, value

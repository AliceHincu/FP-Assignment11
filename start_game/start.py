# ----- IMPORT ZONE -----
from domain.boardJSON import BoardJSON
from validator.boardValidator import validate_column, InvalidColumn
from validator.playerValidator import InvalidInput


# ----- FUNCTION ZONE -----
class Game(BoardJSON):
    def __init__(self):
        super().__init__()
        self._player1_piece = 1
        self._player2_piece = 2
        self._computer_piece = 2

    def next_turn(self, turn):
        """
        --- Description
        Finds out whose turn it's next

        --- Parameters
        :param turn: the actual turn (type: <str>)

        --- Return
        :return: whose turn it's next (type: <str>)
        """
        if self.battle_mode() == "player vs player":
            if turn == 'player1':
                turn = 'player2'
            else:
                turn = 'player1'
        elif self.battle_mode() == "player vs computer":
            if turn == 'player1':
                turn = "player_ai"
            else:
                turn = 'player1'
        return turn

    def play_turn(self, board, turn, col, piece):
        """
        --- Description
        Plays a turn in the game

        --- Parameters
        :param board: (type: <class>)
        :param turn: whose turn is next (type: <str>)
        :param col: the chosen column (type: <int>)
        :param piece: 1 for player1, 2 for player2 and computer (type: <int>)

        --- Return
        :return: - if it is game over or not (type: <bool>)
                 - the board (type: <class>)
                 - the turn (type: <str>)
        """
        try:
            game_over = False
            if validate_column(board, col):
                # drop the piece in the available row
                row = self.get_available_row(board, col)
                self.drop_piece(board, row, col, piece)
                # check for a win
                if self.winning(board, piece):
                    game_over = True
                # it's the opponent's turn
                else:
                    turn = self.next_turn(turn)
                # save
                board.save(turn, self.battle_mode(), self.difficulty())
                return game_over, board, turn

        except (InvalidInput, InvalidColumn) as err:
            print(err)

    def run_game(self, board, turn, col):
        """
        --- Description
        The main program for running the game

        --- Parameters
        :param board: (type: <class>)
        :param turn: whose turn is next (type: <str>)
        :param col: the chosen column (type: <int>)

        --- Return
        :return: - if it is game over or not (type: <bool>)
                 - the board (type: <class>)
                 - the turn (type: <str>)
        """
        game_over = False
        if turn == 'player1':
            game_over, board, turn = self.play_turn(board, turn, col, self._player1_piece)

        elif turn == "player2":
            game_over, board, turn = self.play_turn(board, turn, col, self._player2_piece)

        elif turn == "player_ai":
            game_over, board, turn = self.play_turn(board, turn, col, self._computer_piece)

        return game_over, board, turn

    @staticmethod
    def new_game():
        """
        --- Description
        Create a new board and make player1 play first

        --- Return
        :return: - the board (type: <class>)
                 - the turn (type: <str>)
        """
        # create board
        board = BoardJSON()
        board.create_board()
        turn = 'player1'
        return board, turn

    @staticmethod
    def load_game():
        """
        --- Description
        Load the board and find whose turn it is and find the battle_mode

        --- Return
        :return: - the board (type: <class>)
                 - the turn (type: <str>)
        """
        # create board
        board = BoardJSON()
        if board.boardmatrix() is None:
            board.create_board()
        turn = board.turn()
        battle_mode = board.battle_mode()
        return board, turn, battle_mode


# ----- START THE GAME -----
# def start_game():
#     try:
#         import UI.UI
#         user_interface = UI.UI.UI()
#         mode = user_interface.game_mode()
#         mode = validate_mode(mode, "game_mode")
#         if mode == 1:
#             new_game()
#         else:
#             load_game()
#     except InvalidInputMode as err:
#         print(err)

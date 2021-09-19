# ----- IMPORT ZONE -----
import numpy as np
import math
import time
import colorama
from termcolor import colored

from validator.playerValidator import validate_input, InvalidInputMode, validate_mode
from start_game.start import Game
from start_game.minimax import EasyMode, MediumMode, HardMode


# ----- UI ZONE -----
class UI(Game):
    def __init__(self):
        super().__init__()
        self._ai = None

    def set_ai(self):
        """
        Set the class of ai
        """
        difficulty = self.difficulty()
        if difficulty == "easy":
            self._ai = EasyMode()
        elif difficulty == "medium":
            self._ai = MediumMode()
        elif difficulty == "hard":
            self._ai = HardMode()

    # ----- READ COMMANDS -----
    @staticmethod
    def read_player_move(player):
        """
        --- Description
        Read the player's move

        --- Parameters
        :param player: player1 or player2 (type: <str>)

        --- Returns
        :return: the column (type:str)
        """
        if player == 'player1':
            print(colored("\n --- PLAYER 1 ---", "blue"))
        elif player == 'player2':
            print(colored("\n --- PLAYER 2 ---", "red"))

        print("> What column are you choosing? (0-6)")

        column = input("\tcolumn:")
        return column

    def read_computer_move(self, board):
        """
        --- Description
        Read the computer's move

        --- Parameters
        :param board: the board (type: <class>)

        --- Returns
        :return: the column (type:str)
        """
        print(colored("\n --- COMPUTER ---", "red"))
        print("> What column are you choosing? (0-6)")
        op = ""
        if self.difficulty() == "easy":
            op = self._ai.calculate_move(board)
        elif self.difficulty() == "medium":
            op = self._ai.pick_best_move(board, 2)
        elif self.difficulty() == "hard":
            op, minimax_score = self._ai.minimax(board, 3, math.inf, -math.inf, True)
        print("\n> Computer chose column number " + colored(str(op), "green"))
        return op

    # ----- CHOOSE MODES (MENU MODES) -----
    @staticmethod
    def game_mode():
        """
        --- Description
        Choose game mode

        ---- Returns
        :return: new_game or load_game (type: <str>)
        """
        try:
            print("\n Choose an option:")
            print("\t 1. New game")
            print("\t 2. Load game")
            option = input(" >your option: ")
            option = validate_mode(option, "game_mode")
            if option == 1:
                return "new_game"
            elif option == 2:
                return "load_game"
        except InvalidInputMode as err:
            print(err)

    @staticmethod
    def player_mode():
        """
        --- Description
        Choose player mode

        --- Returns
        :return: one_player or two_players (type: <str>)
        """
        try:
            print("\n Choose an option:")
            print("\t 1.One player")
            print("\t 2.Two players")
            option = input(" >your option: ")
            option = validate_mode(option, "player_mode")
            if option == 1:
                return "one_player"
            elif option == 2:
                return "two_players"
        except InvalidInputMode as err:
            print(err)

    @staticmethod
    def difficulty_mode():
        """
        --- Description
        Choose difficulty

        --- Returns
        :return: easy, medium or hard (type: <str>)
        """
        try:
            print("\n Choose a difficulty:")
            print("\t 1.Easy")
            print("\t 2.Medium")
            print("\t 3.Hard")
            option = input(" >your option: ")
            option = validate_mode(option, "difficulty_mode")
            if option == 1:
                return "easy"
            elif option == 2:
                return "medium"
            elif option == 3:
                return "hard"
        except InvalidInputMode as err:
            print(err)

    # ----- PRINT ----
    @staticmethod
    def color_sign(x):
        """
        --- Description
        Colors the elements in the matrix

        --- Parameters
        :param x: the element (type: <float>)

        -Returns
        :return: blue for the first player, red for second player/computer (type: <int>)
        """
        c = colorama.Fore.LIGHTBLUE_EX if x == 1 else \
            colorama.Fore.RED if x == 2 else \
            colorama.Fore.WHITE
        return f'{c}{int(x)}'

    def print_board(self, board):
        np.set_printoptions(formatter={'float': self.color_sign})
        print(np.flip(board.boardmatrix(), 0))

    @staticmethod
    def win_players(turn):
        if turn == 'player1' or turn == 'player2':
            sentence = "Congratulations! " + turn + str(' wins!!!!!!!!')
            print(colored(sentence, 'green'))
        else:
            sentence = "Oh no, you lost :(("
            print(colored(sentence, 'red'))

    @staticmethod
    def print_reminder(battle_mode):
        print("\nYou are now playing", colored(battle_mode, "green"))

    # ----
    def start_game_ui(self, board, turn):
        game_over = False
        while not game_over:
            try:
                col = 0
                if turn == 'player1' or turn == 'player2':
                    col = self.read_player_move(turn)
                elif turn == "player_ai":
                    time.sleep(1.5)
                    col = self.read_computer_move(board)
                col = validate_input(board, str(col))
                game_over, board, turn = self.run_game(board, turn, col)
                self.print_board(board)
            except ValueError as err:
                print(err)
        self.win_players(turn)
        board.create_board()

    def main_menu_ui(self):
        """
        --- Description
        It shows 3 menus:
            -Main Menu with new game/load game
            -Player menu with one player/two players
            -Difficulty menu with easy/medium/hard mode
        """
        game_over = False
        while not game_over:
            mode = self.game_mode()
            board = None
            turn = None
            # -- new game --
            if mode == "new_game":
                players = self.player_mode()
                board, turn = self.new_game()

                if players == "two_players":
                    self.set_battle_mode("player vs player")

                elif players == "one_player":
                    difficulty = self.difficulty_mode()
                    self.set_dif(difficulty)
                    self.set_ai()
                    self.set_battle_mode("player vs computer")

            # -- load game --
            elif mode == "load_game":
                board, turn, battle_mode = self.load_game()
                self.print_reminder(battle_mode)
                self.print_board(board)
                if battle_mode == 'player vs computer':
                    self.set_ai()

            # -- start game --
            self.start_game_ui(board, turn)
            game_over = True

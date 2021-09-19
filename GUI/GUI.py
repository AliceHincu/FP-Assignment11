# ---- IMPORT ZONE ----
import pygame
from win32api import GetSystemMetrics
from start_game.start import Game
from start_game.minimax import EasyMode, MediumMode, HardMode
import math
import numpy as np


# ---- CLASS ZONE ----
class GuiElements(Game):
    def __init__(self):
        super().__init__()
        self._DISPLAY_WIDTH = GetSystemMetrics(0)
        self._DISPLAY_HEIGHT = GetSystemMetrics(1)
        self._GAME_DISPLAY = pygame.display.set_mode((self._DISPLAY_WIDTH, self._DISPLAY_HEIGHT))
        self._SQUARE_SIZE = 100
        self._RADIUS = self._SQUARE_SIZE / 2 - 5
        self._transparent_black = (0, 0, 0, 200)
        self._black = (0, 0, 0, 255)
        self._white = (255, 255, 255)
        self._blue = (0, 0, 200)
        self._purple = (221, 160, 221)
        self._indigo = (138, 43, 226)

    # --- getters ----
    def game_display(self):
        return self._GAME_DISPLAY

    def display_width(self):
        return self._DISPLAY_WIDTH

    def display_height(self):
        return self._DISPLAY_HEIGHT

    def square_size(self):
        return self._SQUARE_SIZE

    # --- objects ---
    def button(self, msg, color, x, y, w, h, ic, ac, action=None, actionArgs=None):
        """
        Creates a button
        :param msg: What do you want the button to say on it (type: <str>)
        :param color: The color of the text inside the button
        :param x: The x location of the top left coordinate of the button box (type: <int>)
        :param y: The y location of the top left coordinate of the button box (type: <int>)
        :param w: Button width (type: <int>)
        :param h: Button height (type: <int>)
        :param ic: Inactive color (when a mouse is not hovering)
        :param ac: Active color (when a mouse is hovering)
        :param action: The function that is called after pressing the button
        :param actionArgs: Function arguments (type: tuple)
        :return:
        """
        mouse = pygame.mouse.get_pos()  # position of the mouse
        click = pygame.mouse.get_pressed(5)  # if you click

        rect1 = pygame.Rect(x, y, w, h)
        rect1.center = (x, y)

        shape_surf = pygame.Surface(pygame.Rect(rect1).size, pygame.SRCALPHA)
        # if the cursor is on the button
        if x + w/2 > mouse[0] > x - w/2 and y + h/2 > mouse[1] > y - h/2:
            pygame.draw.rect(shape_surf, ac, shape_surf.get_rect())

            if click[0] == 1:
                if actionArgs is not None:
                    action(actionArgs)
                else:
                    action()
        else:
            pygame.draw.rect(shape_surf, ic, shape_surf.get_rect())

        self._GAME_DISPLAY.blit(shape_surf, rect1)
        # the text on the buttons

        self.text("comicsansms", 30, msg, color, x, y)

    def text(self, font, font_size, text, color, x, y):
        """
        Display the text on screen

        ---Variables:
        :param font: the name of the font (type: <str>)
        :param font_size: the size of the font (type: <int>)
        :param text: the text to be displayed (type: <str>)
        :param color: the color of the text (type: <str>)
        :param x: The x location of the center coordinate of the text (type: <int>)
        :param y: The y location of the center coordinate of the text (type: <int>)
        """
        font_text = pygame.font.SysFont(font, font_size)
        text_surf, text_rect = self.text_objects(text, font_text, color)
        text_rect.center = (x, y)
        self._GAME_DISPLAY.blit(text_surf, text_rect)

    def background(self, img):
        """
        Load an image as the background
        :param img: the name of the image file (type: <str>)
        """
        bg = pygame.image.load(img)

        # INSIDE OF THE GAME LOOP
        self.game_display().blit(bg, (0, 0))

    def mini_background(self, x, y, w, h):
        """
        Create a mini background which is a Rect

        --- Variables
        :param x: The x location of the top left coordinate of the mini background (type: <int>)
        :param y: The y location of the top left coordinate of the mini background (type: <int>)
        :param w: Mini background width (type: <int>)
        :param h: Mini background height (type: <int>)
        """
        rect1 = pygame.Rect(x, y, w, h)
        rect1.center = (x, y)
        shape_surf = pygame.Surface(pygame.Rect(rect1).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, self._black, shape_surf.get_rect())
        self._GAME_DISPLAY.blit(shape_surf, rect1)

    def draw_circle(self, pos_x, turn):
        """
        Draw a circle (drop piece)
        :param pos_x: the center in the axis Ox of the circle
        :param turn: who needs to play
        """
        self.mini_background(self._DISPLAY_WIDTH / 2, 100, self._DISPLAY_WIDTH / 2, 200)
        if turn == 'player1':
            pygame.draw.circle(self._GAME_DISPLAY, self.color('player1 color'),
                               (pos_x, 100 + self._SQUARE_SIZE / 2), self._RADIUS)
        else:
            pygame.draw.circle(self._GAME_DISPLAY, self.color('player2 color'),
                               (pos_x, 100 + self._SQUARE_SIZE / 2), self._RADIUS)
        self.text("comicsansms", 30, turn + str('\'s turn'), self._white, self._DISPLAY_WIDTH / 2, 50)

    # --- getter ---
    def color(self, color):
        """
        Returns color
        :param color: the name of the color (type: <str>)
        :return: RGB value
        """
        if color == 'black':
            return self._black
        if color == 'transparent_black':
            return self._transparent_black
        if color == 'white':
            return self._white
        if color == 'player1 color':
            return self._purple
        if color == 'player2 color' or color == 'ai color':
            return self._indigo
        if color == 'board color':
            return self._blue

    # --- helpful functions for objects ---
    @staticmethod
    def text_objects(text, font, color):
        """
        Creates a new Surface with the specified text rendered on it
        :param text: the text (type: <str>)
        :param font: the font (type: <class 'pygame.font.Font'>)
        :param color: the color of the text (type: <str>)
        :return: a new surface (type: <class 'pygame.Surface'>)
                 a new rect with the size of the image and the x, y coordinates (0, 0) (type: <class 'pygame.Rect'>)
        """
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()


class GUI(GuiElements):
    def __init__(self):
        super().__init__()
        self._ai = None
        self._board = None
        self._turn = None
        self._button_clicked = "start_main_menu"
        self._button_clicked_arg = None

    # ---- QUIT ----
    @staticmethod
    def quit_game():
        """
        Quit the game
        """
        pygame.quit()
        quit()

    # ---- WIN ----
    def gui_winning(self, turn):
        """
        When someone wins
        :param turn: the player who won (type: <str>)
        """
        self.create_board()
        self.mini_background(self.display_width() / 2, 100, self.display_width() / 2, 200)
        self.text("comicsansms", 30, turn + str(' wins!!!!!!!!'), self.color('white'), self.display_width() / 2, 50)
        pygame.display.update()
        pygame.time.wait(2000)
        self.main_menu()

    # ---- DRAW BOARD ----
    def draw_board(self, board):
        """
        Draw the board
        :param board: type: <class>
        """
        radius = self.square_size() / 2 - 5
        matrix = np.flip(board.boardmatrix(), 0)
        for c in range(self.columncount()):
            for r in range(self.rowcount()):
                rect_x = c * self.square_size() + 415
                rect_y = self.square_size()*(r+1)+100
                pygame.draw.rect(self.game_display(), self.color('board color'),
                                 (rect_x, rect_y, self.square_size(), self.square_size()))
                if matrix[r][c] == 0:
                    pygame.draw.circle(self.game_display(), self.color('black'),
                                       (rect_x + self.square_size()/2, rect_y + self.square_size()/2), radius)
                elif int(matrix[r][c]) == 1:
                    pygame.draw.circle(self.game_display(), self.color('player1 color'),
                                       (rect_x + self.square_size()/2, rect_y + self.square_size()/2), radius)
                else:
                    pygame.draw.circle(self.game_display(), self.color('player2 color'),
                                       (rect_x + self.square_size() / 2, rect_y + self.square_size() / 2), radius)
        pygame.display.update()

    # ---- MANAGE THE GAME ----
    def player_turn(self, board, turn, event):
        """
        --- Description
        Execute player's turn

        --- Parameters
        :param board: (type: <class>)
        :param turn: either player1 or player2 (type: <str>)
        :param event: get the events from the screen (from pygame)

        --- Return
        :return: if it is game over or not, the board, the turn
        """
        game_over = False
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEMOTION:
            pos_x = event.pos[0]
            if 460 < pos_x < 1075:
                self.draw_circle(pos_x, turn)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_x = event.pos[0]
            col = int(math.floor((pos_x - 415) / self.square_size()))
            if 460 < pos_x < 1075:
                game_over, board, turn = self.run_game(board, turn, col)
                self.draw_circle(pos_x, turn)
                self.draw_board(board)
        return game_over, board, turn

    def computer_turn(self, board, turn):
        """
        --- Description
        Execute player's turn

        --- Parameters
        :param board: (type: <class>)
        :param turn: either player1 or player2 (type: <str>)

        --- Return
        :return: if it is game over or not, the board, the turn
        """
        op = None
        if self.difficulty() == "easy":
            op = self._ai.calculate_move(board)
        elif self.difficulty() == "medium":
            op = self._ai.pick_best_move(board, 2)
        elif self.difficulty() == "hard":
            op, minimax_score = self._ai.minimax(board, 3, math.inf, -math.inf, True)
        game_over, board, turn = self.run_game(board, turn, op)
        return game_over, board, turn

    def gui_run_game(self, board, turn):
        """
        --- Description
        The main function for the game, processing the information

        --- Parameters
        :param board: type: <class>
        :param turn: type: <str>
        """
        game_over = False
        self._button_clicked = "start_main_menu"
        self.game_display().fill(self.color('white'))
        self.background("../GUI/galaxy.jpg")
        self.mini_background(self.display_width() / 2, self.display_height() / 2, self.display_width() / 2,
                             self.display_height())
        self.draw_board(board)
        pygame.display.update()
        while not game_over:
            for event in pygame.event.get():
                game_over, board, turn = self.player_turn(board, turn, event)

            if turn == 'player_ai':
                self.mini_background(self.display_width() / 2, 100, self.display_width() / 2, 200)
                pygame.time.wait(1000)
                game_over, board, turn = self.computer_turn(board, turn)
                self.draw_circle(self.display_width()/2, turn)

            self.button("x", "white", 1400, 100, 50, 50, self.color('transparent_black'), self.color('black'),
                        self.quit_game)
            self.draw_board(board)
            pygame.display.update()

        self.gui_winning(turn)
        self.quit_game()

    def gui_load_game(self):
        """
        Load the game. If the game doesn't exist, it creates a new one
        """
        board, turn, battle_mode = self.load_game()
        if battle_mode == 'player vs computer':
            self.set_ai(self.difficulty())
        self.gui_run_game(board, turn)

    # --- FUNCTION FOR SWITCHING MENUS ---
    def change_button_clicked(self, func_args=None):
        if isinstance(func_args, str):
            self._button_clicked = str(func_args)
        else:
            self._button_clicked = str(func_args[0])
            self._button_clicked_arg = func_args[1]
        pygame.time.wait(540)

    # --- SET AI ---
    def set_ai(self, dif):
        """
        Set the class of ai
        """
        difficulty = dif
        if difficulty == "easy":
            self._ai = EasyMode()
        elif difficulty == "medium":
            self._ai = MediumMode()
        elif difficulty == "hard":
            self._ai = HardMode()
        self.set_dif(dif)
        self._button_clicked = "run_new_game"

    # --- MENU STUFF ---
    def gui_difficulty_menu(self):
        """
        --- Description
        Choose from easy, medium or hard
        """
        self.game_display().fill(self.color('white'))
        self.background("../GUI/galaxy.jpg")
        self.text("gabriola", 215, "Connect Four", "black", (self.display_width() / 2), (self.display_height() / 4))
        self.text("gabriola", 215, "Connect Four", "white", (self.display_width() / 2 + 15),
                  (self.display_height() / 4))

        self.button("Easy", "white", (self.display_width() / 2), (self.display_height() / 2), 300, 100,
                    self.color('transparent_black'), self.color('black'), self.change_button_clicked,
                    ("set_ai", "easy"))
        self.button("Medium", "white", (self.display_width() / 2), (self.display_height() * 2 / 3), 300, 100,
                    self.color('transparent_black'), self.color('black'), self.change_button_clicked,
                    ("set_ai", "medium"))
        self.button("Hard", "white", (self.display_width() / 2), (self.display_height() * 5 / 6), 300, 100,
                    self.color('transparent_black'), self.color('black'), self.change_button_clicked,
                    ("set_ai", "hard"))
        pygame.display.update()

    def gui_choose_battle_mode(self, ai_exists):
        """
        --- Description
        Menu for choosing the battle mode.
        Options: player vs player or computer vs computer
        """
        if ai_exists:
            self.set_battle_mode("player vs computer")
            self._button_clicked = "gui_difficulty_menu"
        else:
            self.set_battle_mode("player vs player")
            self._button_clicked = "run_new_game"

    def start_battle_mode_menu(self):
        """
        --- Description
        Menu for choosing the battle mode(player vs player or player vs computer)
        Buttons: one player, two players, quit game
        """
        self.game_display().fill(self.color('white'))
        self.background("../GUI/galaxy.jpg")
        self.text("gabriola", 215, "Connect Four", "black", (self.display_width() / 2), (self.display_height() / 4))
        self.text("gabriola", 215, "Connect Four", "white", (self.display_width() / 2 + 15),
                  (self.display_height() / 4))

        self.button("One player", "white", (self.display_width() / 2), (self.display_height() / 2), 300, 100,
                    self.color('transparent_black'), self.color('black'), self.change_button_clicked,
                    ("gui_choose_battle_mode", True))
        self.button("Two players", "white", (self.display_width() / 2), (self.display_height() * 2 / 3), 300, 100,
                    self.color('transparent_black'), self.color('black'), self.change_button_clicked,
                    ("gui_choose_battle_mode", False))
        self.button("Quit game", "white", (self.display_width() / 2), (self.display_height() * 5 / 6), 300, 100,
                    self.color('transparent_black'), self.color('black'), self.change_button_clicked,
                    "quit_game")
        pygame.display.update()

    def main_menu(self):
        """
        --- Description
        Shows the buttons for the main menu: new game, load game, quit game
        """
        self.game_display().fill(self.color('white'))
        self.background("../GUI/galaxy.jpg")
        self.text("gabriola", 215, "Connect Four", "black", (self.display_width() / 2), (self.display_height() / 4))
        self.text("gabriola", 215, "Connect Four", "white", (self.display_width() / 2 + 15),
                  (self.display_height() / 4))

        self.button("New game", "white", (self.display_width() / 2), (self.display_height() / 2), 300, 100,
                    self.color('transparent_black'), self.color('black'), self.change_button_clicked,
                    "start_battle_mode_menu")
        self.button("Load game", "white", (self.display_width() / 2), (self.display_height() * 2 / 3), 300, 100,
                    self.color('transparent_black'), self.color('black'), self.change_button_clicked,
                    "gui_load_game")
        self.button("Quit game", "white", (self.display_width() / 2), (self.display_height() * 5 / 6), 300, 100,
                    self.color('transparent_black'), self.color('black'), self.change_button_clicked,
                    "quit_game")

        pygame.display.update()

    def gui_start_main_menu(self):
        """
        Show the windows (menus + game)
        """
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if self._button_clicked == "start_main_menu":
                self.main_menu()

            # --- Main Menu ---
            elif self._button_clicked == "start_battle_mode_menu":
                self.start_battle_mode_menu()
            elif self._button_clicked == "gui_load_game":
                self.gui_load_game()
            elif self._button_clicked == "quit_game":
                self.quit_game()

            # --- Start Battle Mode Menu ---
            elif self._button_clicked == "gui_choose_battle_mode":
                self.gui_choose_battle_mode(self._button_clicked_arg)

            # --- Difficulty Menu ---
            elif self._button_clicked == "gui_difficulty_menu":
                self.gui_difficulty_menu()
            elif self._button_clicked == "set_ai":
                self.set_ai(self._button_clicked_arg)

            # --- Run game ---
            if self._button_clicked == "run_new_game":
                board, turn = self.new_game()
                self.create_board("player1", self.battle_mode())
                self.gui_run_game(board, turn)

    # --- START GUI ---
    def start_gui(self):
        """
        Start the GUI
        """
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("../GUI/main menu music.mp3")
        pygame.mixer.music.play(-1)
        self.gui_start_main_menu()

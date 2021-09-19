# ----- EXCEPTIONS -----
class InvalidInput(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class InvalidInputMode(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# ----- VALIDATION FUNCTIONS -----
def validate_input(board, col):
    """
    Validates the player input
    -- Variables:
    :param board: the board itself (type: class <Board>)
    :param col: the column input from the player (type: <str>)

    --Raises:
    InvalidInput - if the input is not a natural number that belongs to [0,row_count]

    :return: the column if it's ok, an error if not
    """
    if not col.isdigit():
        raise InvalidInput("The input should be a natural number")
    elif not 0 <= int(col) <= board.columncount()-1:
        raise InvalidInput('The input should belong to the interval [0,' + str(board.columncount()-1) + ']')
    else:
        return int(col)


def validate_mode(option, mode):
    """
    Validates the input
    :return: type: <int>
    """
    options = ["1", "2", "3"]
    if mode == "game_mode" or mode == "player_mode":
        if option in options and option != "3":
            return int(option)
        else:
            raise InvalidInputMode("The option should be either 1 or 2")
    elif mode == "difficulty_mode":
        if option in options:
            return int(option)
        else:
            raise InvalidInputMode("The option should be either 1, 2 or 3")
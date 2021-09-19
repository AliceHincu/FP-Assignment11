# ----- EXCEPTIONS -----
class InvalidColumn(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# ----- VALIDATION FUNCTIONS -----
def validate_column(board, col):
    """
    Checks if yhe player can put another piece on top
    -- Variables:
    :param board: the board itself (type: class <Board>)
    :param col: the column input from the player (type: <int>)

    -- Raises:
    InvalidColumn - if the selected column is full

    :return: true if it's ok, false if not (type: <bool>)
    """
    upper_row = board.rowcount() - 1
    matrix = board.boardmatrix()
    if matrix[upper_row][col] != 0:
        raise InvalidColumn('The column is full!')
    else:
        return True

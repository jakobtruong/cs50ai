"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.

    X gets first move when given an initial state of a board
    """
    is_even = True
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] != EMPTY:
                is_even != is_even

    return X if is_even else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                set.add((row, col))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = copy.deepcopy(board)
    player_turn = player(result_board)
    result_board[action[0]][action[1]] = player_turn

    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in range(len(board)):
        if board[row][0] != EMPTY and board[row][0] == board[row][1] == board[row][2]:
            return board[row][0]

    # Checks columns
    for col in range(len(board[0])):
        if board[0][col] != EMPTY and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]

    # Checks major diagonal
    if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    # Checks minor diagonal
    if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    spaces_filled = True
    # Checks rows and also checks if all spaces are not empty
    for row in range(len(board)):
        if board[row][0] != EMPTY and board[row][0] == board[row][1] == board[row][2]:
            return True
        if board[row][0] == EMPTY or board[row][1] == EMPTY or board[row][2] == EMPTY:
            spaces_filled = False

    # Checks columns
    for col in range(len(board[0])):
        if board[0][col] != EMPTY and board[0][col] == board[1][col] == board[2][col]:
            return True

    # Checks major diagonal
    if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return True

    # Checks minor diagonal
    if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return True

    return spaces_filled


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)

    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError

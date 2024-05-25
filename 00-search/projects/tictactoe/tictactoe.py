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
                is_even = not is_even

    return X if is_even else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                possible_actions.add((row, col))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Checks for edge cases where action is a coordinate that is out of bounds or a coordinate that has an X or O already placed
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise Exception("Sorry, action has coordinated that are out of bounds.")
    elif board[action[0]][action[1]] != EMPTY:
        raise Exception("Sorry, a move was already placed here.")

    result_board = copy.deepcopy(board)
    player_turn = player(result_board)
    result_board[action[0]][action[1]] = player_turn

    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checks rows
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

    Maximize if player is X and minimize if player is O

    Optimizations to consider: Alpha-Beta Pruning
    """
    # Helper function to decide best action for player X
    def max_value(board):
        if terminal(board):
            return (utility(board), None)

        value = float('-inf')
        optimal_action = None
        for potential_action in actions(board):
            potential_board = result(board, potential_action)
            potential_board_value = min_value(potential_board)[0]
            if potential_board_value > value:
                value = potential_board_value
                optimal_action = potential_action

        return (value, optimal_action)

    # Helper function to decide best action for player O
    def min_value(board):
        if terminal(board):
            return (utility(board), None)

        value = float('inf')
        optimal_action = None
        for potential_action in actions(board):
            potential_board = result(board, potential_action)
            potential_board_value = max_value(potential_board)[0]
            if potential_board_value < value:
                value = potential_board_value
                optimal_action = potential_action

        return (value, optimal_action)

    current_player = player(board)
    optimal_action = None

    optimal_action = max_value(board)[1] if current_player == X else min_value(board)[1]

    return optimal_action

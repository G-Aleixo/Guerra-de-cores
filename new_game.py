from copy import deepcopy
from typing import Literal

Board = list[list[int]]

def out_of_bounds(pos: list[int, int], size: int) -> bool:
    return (pos[0] < 0 or pos[1] < 0) or (pos[0] >= size or pos[1] >= size)

def get_sign(number: int) -> Literal[-1, 1, 0]:
    if number < 0: return -1
    if number > 0: return 1
    return 0

def add_point(value: int, player: int) -> int:
    return (abs(value) + 1) * player

def get_points(board: Board) -> int:
    score = [0, 0]
    
    for i in range(len(board)):
        for j in range(len(board)):
            sign = get_sign(board[i][j])
            if sign == -1: score[0] += 1
            elif sign == 1: score[1] += 1
    
    return score
def has_lost(score: list[int, int]):
    if score[0] == 0 or score[1] == 0:
        return True

def update_board(board: Board) -> Board:
    """Does a single update tick of the board

    Args:
        board (Board): Board to be updated

    Returns:
        Board: Updated board
    """
    updated_board = deepcopy(board)
    
    board_size = len(board)
    for i in range(board_size):
        for j in range(board_size):
            if abs(board[i][j]) >= 4:
                sign = get_sign(updated_board[i][j])
                updated_board[i][j] -= 4 * sign
                
                if not out_of_bounds([i+1, j], board_size): updated_board[i+1][j] = add_point(board[i+1][j], sign)
                if not out_of_bounds([i-1, j], board_size): updated_board[i-1][j] = add_point(board[i-1][j], sign)
                if not out_of_bounds([i, j+1], board_size): updated_board[i][j+1] = add_point(board[i][j+1], sign)
                if not out_of_bounds([i, j-1], board_size): updated_board[i][j-1] = add_point(board[i][j-1], sign)
    return updated_board

def resolve_board(board: Board) -> list[Board, Literal[-1, 1, 0]]:
    """Updates the board until either a player has won or there is nothing to update

    Args:
        board (Board): Board to be resolved
    """
    temp_board = deepcopy(board)
    
    new_board = update_board(temp_board)
    while temp_board != new_board and (get_points(new_board)[0] != 0 and get_points(new_board)[1] != 0):
        temp_board, new_board = new_board, update_board(new_board)
    
    if get_points(new_board)[0] == 0:
        return [new_board, 1]
    elif get_points(new_board)[1] == 0:
        return [new_board, -1]
    
    return [new_board, 0]
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

def undo_changes(board: Board, changes: list[tuple[int, int, int]]):
    """Undo the changes made to the board."""
    for x, y, value in changes:
        board[x][y] = value

def apply_move(board: Board, move: list[int], player: int) -> list[tuple[int, int, int]]:
    """Apply a move to the board and return the changes made."""
    changes = []
    x, y = move
    changes.append((x, y, board[x][y]))
    changes.append((x, y, board[x][y]))
    changes.append((x, y, board[x][y]))
    if board[x][y] == 0:
        board[x][y] = add_point(board[x][y], player)
        board[x][y] = add_point(board[x][y], player)
    board[x][y] = add_point(board[x][y], player)
    return changes

def update_board(board: Board) -> list[tuple[int, int, int]]:
    """Does a single update tick of the board and returns the changes made."""
    changes = []
    board_size = len(board)
    
    for i in range(board_size):
        for j in range(board_size):
            if abs(board[i][j]) >= 4:
                sign = get_sign(board[i][j])
                changes.append((i, j, board[i][j]))
                board[i][j] -= 4 * sign
                
                if not out_of_bounds([i+1, j], board_size):
                    changes.append((i+1, j, board[i+1][j]))
                    board[i+1][j] = add_point(board[i+1][j], sign)
                if not out_of_bounds([i-1, j], board_size):
                    changes.append((i-1, j, board[i-1][j]))
                    board[i-1][j] = add_point(board[i-1][j], sign)
                if not out_of_bounds([i, j+1], board_size):
                    changes.append((i, j+1, board[i][j+1]))
                    board[i][j+1] = add_point(board[i][j+1], sign)
                if not out_of_bounds([i, j-1], board_size):
                    changes.append((i, j-1, board[i][j-1]))
                    board[i][j-1] = add_point(board[i][j-1], sign)
    
    return changes

def resolve_board(board: Board) -> list[Board, Literal[-1, 1, 0]]:
    """Updates the board until either a player has won or there is nothing to update."""
    temp_board = deepcopy(board)
    
    while True:
        changes = update_board(temp_board)
        if not changes:
            break
        if get_points(temp_board)[0] == 0:
            return [temp_board, 1]
        elif get_points(temp_board)[1] == 0:
            return [temp_board, -1]
    
    return [temp_board, 0]
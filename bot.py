from new_game import *

def get_possible_moves(board: Board, player: int):
    possible_moves = []
    
    for i in range(len(board)):
        for j in range(len(board)):
            if get_sign(board[i][j]) == player:
                possible_moves.append([i, j])
    return possible_moves

def minimax(board: Board, player: int, depth: int):
    if depth == 0:
        return float('inf')

    scores = []
    best_move = None
    
    possible_moves = get_possible_moves(board, player)
    for move in possible_moves:
        print(f"{move}: {get_possible_moves(board, -player)}")
    return possible_moves


board = [[3,3,3],[3,3,3],[3,3,3]]
board = resolve_board(board)[0]
print(board)
board[0][0] = add_point(board[0][0], 1)
print(board)
board = resolve_board(board)[0]
print(board)
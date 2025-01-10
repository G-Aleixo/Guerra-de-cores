from math import inf
from game import *
from time import time

MAX = 1
MIN = -1
MAX_DEPTH = 9 # should work good? didn't test

DEBUG = False

possibilities_searched = 0
branches_pruned = 0

def get_positional_scores(board_size: int) -> list[list[int]]:
    values = [[2 for _ in range(board_size)] for _ in range(board_size)]
    
    for i in range(board_size):
        for j in range(board_size):
            if i != 0 and i != board_size - 1:
                values[i][j] += 1
            if j != 0 and j != board_size - 1:
                values[i][j] += 1
    return values

def get_possible_moves(board: Board, player: int, is_first_move: bool = False):
    possible_moves = []
    
    if is_first_move:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    possible_moves.append([i, j])
        return possible_moves
    
    for i in range(len(board)):
        for j in range(len(board)):
            if get_sign(board[i][j]) == player:
                possible_moves.append([i, j])
    return possible_moves

def get_score(board: Board):
    win = get_points(board)
    
    if win[0] == 0:
        return +inf
    elif win[1] == 0:
        return -inf
    
    pos_mult = get_positional_scores(len(board))
    
    score = 0
    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] < 0:
                score -= board[i][j]**2 * pos_mult[i][j] / 4
            elif board[i][j] > 0:
                score += board[i][j]**2 * pos_mult[i][j] / 4
    
    return score
    

def minimax(board: Board, player: int, depth: int, alpha: int = -inf, beta: int = +inf, moves_passed: int = 2):
    global possibilities_searched, branches_pruned
    
    if player == MAX:
        best = [-1, -1, -inf, +inf]
    else:
        best = [-1, -1, +inf, +inf]
    # [x, y, score, depth]
        
    if depth >= MAX_DEPTH or (has_lost(get_points(board)) and not moves_passed < 2):
        return [-1, -1, get_score(board), depth]
    
    if moves_passed < 2:
        possible_moves = get_possible_moves(board, player, True)
    else:
        possible_moves = get_possible_moves(board, player)
    
    for move in possible_moves:
        if DEBUG: possibilities_searched += 1
        
        x, y = move[0], move[1]
        changes = apply_move(board, move, player)
        minimax_board, won = resolve_board(board)
        score = minimax(minimax_board, -player, depth+1, alpha, beta, moves_passed + 1)
        undo_changes(board, changes)
        
        score[0], score[1] = x, y

        if player == MAX:
            if score[2] > best[2]:
                best = score
            elif score[2] == best[2]:
                if score[3] < best[3]:
                    best = score
            
            alpha = max(alpha, best[2])
        
        else:
            if score[2] < best[2]:
                best = score
            elif score[2] == best[2]:
                if score[3] < best[3]:
                    best = score
            
            beta = min(beta, best[2])
        if beta <= alpha:
            if DEBUG: branches_pruned += 1
            break
        
    return best

if __name__ == "__main__":

    def initiate_game_loop(board):
        global possibilities_searched, branches_pruned
        
        move = [int(x) for x in input("your move:").split()]
        board[move[0]][move[1]] += 3
        
        if DEBUG:
            print("optimal enemy move:")
            before_time = time()
        result = minimax(board, MIN, 0, moves_passed=1)
        if DEBUG:
            print(result)
            print(f"pruned {branches_pruned} branches and seen through {possibilities_searched} futures in {round(time()-before_time, 2)} seconds")
            possibilities_searched = 0
            branches_pruned = 0
        
        move = result[0:2]
        
        board[move[0]][move[1]] -= 3
        board = resolve_board(board)[0]
        
        # reference board
        for i in board:
            print(i)
        
        while True:
            move = [int(x) for x in input("your move:").split()]
            
            board[move[0]][move[1]] += 1
            board = resolve_board(board)[0]
            
            if has_lost(get_points(board)): break
            
            print("optimal enemy move:")
            before_time = time()
            result = minimax(board, MIN, 0)
            print(result)
            print(f"pruned {branches_pruned} branches and seen through {possibilities_searched} futures in {round(time()-before_time, 2)} seconds")
            possibilities_searched = 0
            branches_pruned = 0
            
            move = result[0:2]
            
            board[move[0]][move[1]] -= 1
            board = resolve_board(board)[0]
            
            # reference board
            for i in board:
                print(i)
            
            if has_lost(get_points(board)): break
        
        if get_points(board)[0] == 0:
            print("You won!")
        if get_points(board)[1] == 0:
            print("You lost :(")

    initiate_game_loop(board)
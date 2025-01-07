from math import inf
from new_game import *


MAX = 1
MIN = -1
MAX_DEPTH = 7

possibilities_searched = 0

def get_possible_moves(board: Board, player: int):
    possible_moves = []
    
    for i in range(len(board)):
        for j in range(len(board)):
            if get_sign(board[i][j]) == player:
                possible_moves.append([i, j])
    return possible_moves

def get_score(board: Board):
    score = get_points(board)
    
    if score[0] == 0:
        return +inf
    elif score[1] == 0:
        return -inf
    
    return -score[0] + score[1]

def minimax(board: Board, player: int, depth: int, alpha: int = -inf, beta: int = +inf):
    if player == MAX:
        best = [-1, -1, -inf, +inf]
    else:
        best = [-1, -1, +inf, +inf]
    # [x, y, score, depth]
        
    if depth >= MAX_DEPTH or has_lost(get_points(board)):
        return [-1, -1, get_score(board), depth]
    
    possible_moves = get_possible_moves(board, player)
    
    for move in possible_moves:
        global possibilities_searched
        possibilities_searched += 1
        
        x, y = move[0], move[1]
        minimax_board = deepcopy(board)
        minimax_board[x][y] = add_point(minimax_board[x][y], player)
        minimax_board, won = resolve_board(minimax_board)
        # print(" "*(4-depth), minimax_board, won)
        score = minimax(minimax_board, -player, depth+1, alpha, beta)
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
            break
        
    return best

board_size = int(input("What is the board size: "))
board = []
print("insert the board data below")
print("positive numbers for player points and negative for bot points")
for i in range(board_size):
    board.append([int(x) for x in input().split()])

def initiate_game_loop(board):
    global possibilities_searched
    
    while True:
        
        if has_lost(get_points(board)): break
        
        print("reccomended move:")
        print(minimax(board, MAX, 0)[0:4])
        print(f"searched {possibilities_searched} possibilities")
        possibilities_searched = 0
        
        move = [int(x) for x in input("your move:").split()]
        
        board[move[0]][move[1]] += 1
        board = resolve_board(board)[0]
        
        # reference board
        for i in board:
            print(i)
        
        move = [int(x) for x in input("opponent move:").split()]
        
        board[move[0]][move[1]] -= 1
        board = resolve_board(board)[0]
    
    if get_points(board)[0] == 0:
        print("You won!")
    if get_points(board)[1] == 0:
        print("You lost :(")

initiate_game_loop(board)
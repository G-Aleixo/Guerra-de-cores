from game import *
from minimax import *
from colorama import init

init()

def get_settings() -> dict:
    settings_dict = dict()
    
    with open("config.txt", "r") as settings:
        lines = settings.readlines()
        for line in lines:
            if line:
                identifier = line.split()[0]
                setting = line.split()[1]
                settings_dict[identifier] = int(setting)
    
    return settings_dict

def display_board(board: Board) -> None:
    rep = {
        1: "1",
        2: "2",
        3: "3"
    }
    
    for row in board:
        for point in row:
            if point > 0:
                print(f"\033[34m{rep[point]}\033[0m", end=" ")
            elif point < 0:
                print(f"\033[31m{rep[abs(point)]}\033[0m", end=" ")
            else:
                print("0", end=" ")
        print()

configs = get_settings()
DEPTH = configs["DEPTH"]
DEBUG = configs["DEBUG"]

print("""\
Welcome to color wars!
What game mode do you want:
1- player against bot
2- bot against player (bot goes first)
3- player against player
4- bot against bot
(You may also change some settings in config.txt)""")

gamemode = int(input(""))

print("""\
Do you want to start from a specific position?
[Y]es/[N]o""")
specific_pos: bool = True if input("").lower() == "y" else False
if specific_pos:
    board_size = int(input("What is the board size: "))
    board = []
    print("\nInsert the board data below")
    print("Positive numbers for player points and negative for bot points")
    for i in range(board_size):
        board.append([int(x) for x in input().split()])
else:
    board_size = int(input("What is the board size: "))
    board = [[0 for _ in range(board_size)] for _ in range(board_size)]

match gamemode:
    case 1:
        if not specific_pos:
            move = [int(x) for x in input("Your move:").split()]
            board[move[0]][move[1]] += 3
            
            result = minimax(board, MIN, 0, moves_passed=1)
            
            move = result[0:2]
        
            board[move[0]][move[1]] -= 3
            board = resolve_board(board)[0]
            
            # reference board
            display_board(board)
        
        
        while True:
            move = [int(x) for x in input("Your move:").split()]
            
            while not valid_move(board, move, 1):
                print("Invalid move!")
                move = [int(x) for x in input("Your move:").split()]
            board[move[0]][move[1]] += 1
            board = resolve_board(board)[0]
            
            if has_lost(get_points(board)): break
            
            if DEBUG:
                print("Optimal enemy move:")
                before_time = time()
            result = minimax(board, MIN, DEPTH)
            if DEBUG:
                print(result)
                print(f"Pruned {branches_pruned} branches and seen through {possibilities_searched} futures in {round(time()-before_time, 2)} seconds")
                possibilities_searched = 0
                branches_pruned = 0
            if result[2] == inf or result[2] == -inf:
                print(f"Position evaluation: Victory in {result[3]} moves")
            if result[2] == -inf:
                print(f"Position evaluation: Defeat in {result[3]} moves")
            else:
                print(f"Position evaluation: {result[2]}")
            
            move = result[0:2]
            
            board[move[0]][move[1]] -= 1
            board = resolve_board(board)[0]
            
            # reference board
            display_board(board)
            
            if has_lost(get_points(board)): break
        
        if get_points(board)[0] == 0:
            print("You won!")
        if get_points(board)[1] == 0:
            print("You lost :(")
    
    case 3:
        if not specific_pos:
            move = [int(x) for x in input("First player move:").split()]
            board[move[0]][move[1]] += 3
            
            move = [int(x) for x in input("Second player move:").split()]
            board[move[0]][move[1]] -= 3
            
        while True:
            # reference board
            display_board(board)
            move = [int(x) for x in input("Player 1 move:").split()]
            
            while not valid_move(board, move, 1):
                print("Invalid move!")
                move = [int(x) for x in input("Player 1 move:").split()]
            board[move[0]][move[1]] += 1
            board = resolve_board(board)[0]
            
            if has_lost(get_points(board)): break
            
            # reference board
            display_board(board)
            move = [int(x) for x in input("Player 2 move:").split()]
            
            while not valid_move(board, move, -1):
                print("Invalid move!")
                move = [int(x) for x in input("Player 2 move:").split()]
            board[move[0]][move[1]] -= 1
            board = resolve_board(board)[0]
            
            if has_lost(get_points(board)): break
        
        if get_points(board)[1] == 0:
            print("Player 2 won!")
        if get_points(board)[0] == 0:
            print("Player 1 won!")
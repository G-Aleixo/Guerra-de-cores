import game
import os

cls = lambda: os.system("cls") if os.name == "nt" else os.system("clear")

board: game.Game = game.Game(6)

pos1 = [int(indice) for indice in input("Onde o jogador 1 começara?\n").split()]
pos2 = [int(indice) for indice in input("Onde o jogador 2 começara?\n").split()]

board.setup_game(pos1, pos2)

current_player: int = 1
win: bool = False
cls()
while not win:
    cls()
    board.display_board()
    
    pos = [int(indice) for indice in input(f"Where will player {int(-current_player / 2 + 1.5)} play?\n").split()]
    
    board.add_point_to(current_player, pos)
    current_player *= -1
    
    win, winning_player = board.has_won()
cls()
board.display_board()
print(f"Player {int(-current_player / 2 + 1.5)} has won!")
import game

board = game.Game(3)

board.setup_game([1, 2], [1, 1])

board.display_board()

board.add_point_to(-1, [1, 1])

board.display_board()

print(board.has_won())
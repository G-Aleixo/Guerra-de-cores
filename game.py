position = list[int, int]

# Board data is stored in an int as playernumber << 2 + points, with 0 points acctually being 1 point and to represent actual zero points just use a value of zero
# n: player number
# p: point data
# nnnnnnpp
# May change if the point limit changes

def is_inside_box(box_size: list[int, int], pos: position) -> bool:
    if pos[0] < 0 or pos[1] < 0: return False
    if pos[0] >= box_size or pos[1] >= box_size: return False
    return True

class Game:
    def __init__(self, board_size: int, player_amount: int = 2) -> None:
        self.start: bool = True
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.player_amount = 2
        
        self.__POINT_LIMIT = 4
    def setup_game(self, player1: position, player2: position) -> None:
        """
        Sets the player's starting points starting with player 1 and then player 2\n
        WARNING: Validate the players positions before using this function.

        Args:
            player1 (position): _description_
            player2 (position): _description_
        """
        self.board[player1[0]][player1[1]] = 1 << 2 | self.__POINT_LIMIT - 2
        self.board[player2[0]][player2[1]] = 2 << 2 | self.__POINT_LIMIT - 2
    def add_point_to(self, player: int, pos: position) -> None:
        if not is_inside_box(len(self.board), pos):
            return
        if self.board[pos[0]][pos[1]] == 0:
            self.board[pos[0]][pos[1]] = player << 2
        else:
            self.board[pos[0]][pos[1]] = player << 2 | ( 0b11 & (self.board[pos[0]][pos[1]] + 1))
        
        if self.board[pos[0]][pos[1]] & 0b11 >= self.__POINT_LIMIT - 1:
            self.board[pos[0]][pos[1]] = 0
            
            #TODO: Change from recursive to iterative function
            self.add_point_to(player, [pos[0] - 1, pos[1]])
            self.add_point_to(player, [pos[0], pos[1] - 1])
            self.add_point_to(player, [pos[0] + 1, pos[1]])
            self.add_point_to(player, [pos[0], pos[1] + 1])
    def display_board(self) -> None:
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                point_string = (self.board[i][j] & 0b11) + 1 if self.board[i][j] != 0 else 0
                print(f"\033[{30 + (self.board[i][j] >> 2)}m{point_string}\033[39m", end=" ")
            print()
    def has_won(self) -> list[bool, int]:
        player_count = [0, 0]
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] >> 2 != 0: player_count[(self.board[i][j] >> 2) - 1] += 1
                if player_count[0] != 0 and player_count[1] != 0:
                    return [False, 0]
        if player_count[0] != 0: return [True, 1]
        return [True, 2]
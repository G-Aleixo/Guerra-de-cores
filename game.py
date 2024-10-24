position = list[int, int]

def is_inside_box(box_size: list[int, int], pos: position) -> bool:
    if pos[0] < 0 or pos[1] < 0: return False
    if pos[0] >= box_size or pos[1] >= box_size: return False
    return True

class Game:
    def __init__(self, board_size: int, player_amount: int = 2) -> None:
        self.start: bool = True
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        # self.board stores player values as positive from player 1 and negative for player 2
        self.__POINT_LIMIT = 4
    def setup_game(self, player1: position, player2: position) -> None:
        """
        Sets the player's starting points starting with player 1 and then player 2\n
        WARNING: Validate the players positions before using this function.

        Args:
            player1 (position): _description_
            player2 (position): _description_
        """
        self.board[player1[0]][player1[1]] = self.__POINT_LIMIT - 1
        self.board[player2[0]][player2[1]] = -self.__POINT_LIMIT + 1
    def add_point_to(self, player: int, pos: position) -> None:
        if not is_inside_box(len(self.board), pos):
            return
        self.board[pos[0]][pos[1]] = (abs(self.board[pos[0]][pos[1]]) + 1) * player
        
        if abs(self.board[pos[0]][pos[1]]) >= self.__POINT_LIMIT:
            self.board[pos[0]][pos[1]] -= self.__POINT_LIMIT * player
            
            self.add_point_to(player, [pos[0] - 1, pos[1]])
            self.add_point_to(player, [pos[0], pos[1] - 1])
            self.add_point_to(player, [pos[0] + 1, pos[1]])
            self.add_point_to(player, [pos[0], pos[1] + 1])
    def display_board(self) -> None:
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] < 0:
                    print(f"{self.board[i][j]}", end=" ")
                else:
                    print(f" {self.board[i][j]}", end=" ")
            print()
    def has_won(self) -> list[bool, int]:
        player_count = [0, 0]
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] > 0: player_count[0] += 1
                if self.board[i][j] < 0: player_count[1] += 1
                if player_count[0] != 0 and player_count[1] != 0:
                    return [False, 0]
        if player_count[0] != 0: return [True, 1]
        return [True, -1]
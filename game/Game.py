from Map import Map
from Player import Player

class Game:

    is_game_finished = False
    is_first_player_win = False
    is_second_player_win = False

    def __init__(self, first_player : Player, second_player : Player) -> None:
        self.__map = Map(8, 10)
        self.__first_player = first_player
        self.__second_player = second_player
    
    def play_game(self):
        is_first_player_move = True
        while self.__map.is_end_of_game():
            if not self.__map.is_continuous_move_possible():
                is_first_player_move = not is_first_player_move
            move = self.__first_player(self.__map) if is_first_player_move else self.__second_player(self.__map)
            self.__map.make_move(move, is_first_player_move)
        self.is_game_finished = True
        self.decide_winner(is_first_player_move)

    def decide_winner(self, is_first_player_move : bool):
        if self.__map.is_goal(True):
            self.is_first_player_win = True
            return

        if self.__map.is_goal(False):
            self.is_second_player_win = True
            return

        if is_first_player_move: # current side can't make a move
            self.is_second_player_win = True
        else:
            self.is_first_player_win = True

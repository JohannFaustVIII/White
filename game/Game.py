from Map import Map
from Player import Player

class Game:

    def __init__(self, first_player : Player, second_player : Player) -> None:
        self.__map = Map(8, 10)
        self.__first_player = first_player
        self.__second_player = second_player
    
    def play(self) -> bool: # is first player win, TODO: refactor
        side = True # is_current_first_player (TODO: think about good name)
        while self.__map.is_end_of_game():
            if not self.__map.is_continuous_move_possible():
                side = not side
            move = self.__first_player(self.__map) if side else self.__second_player(self.__map)
            self.__map.make_move(move, side)
        if self.__map.is_goal(True):
            return True
        if self.__map.is_goal(False):
            return False
        return not side # current side lost?

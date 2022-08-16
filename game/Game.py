from Map import Map
from Player import Player

class Game:

    def __init__(self, first_player : Player, second_player : Player) -> None:
        self.__map = Map(8, 10)
        self.__first_player = first_player
        self.__second_player = second_player
    
    def play(self):
        side = True # is_current_first_player (TODO: think about good name)
        # while is any move possible: (TODO: implement this check in Map)
        #   if continuous move NOT possible:
        #       change player
        #   get move from current player
        #   make a move on the map
        # if is_goal(True): first won
        # if is_goal(False): second won
        # if NOT is_any_move_possible: current side lost
        pass

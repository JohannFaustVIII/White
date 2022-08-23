import random
from Map import Map
from Player import Player

class NNPlayer(Player):

    def __init__(self, discover : float) -> None:
        super().__init__()
        # player's parameters have to be set from the outside
        # 1. here to provide NN and check its parameters? or load here? first option looks better
        self.discover = discover

    def get_move(self, map : Map, first_player : bool) -> int:
        moves = map.get_possible_moves()
        print(moves)
        if random.random() < self.discover:
            print("Random!")
            return random.choice(moves)
        else:
            print("Value!")
            valued_moves = [(move, random.random(), map.get_points_for_move(move, first_player)) for move in moves] # the state pass to NN, get state prediction from NN (value between 0 to 1, 0 - state lost, 1 - state win)
            max_move = max(valued_moves, key=lambda x: x[1])
            return max_move[0]
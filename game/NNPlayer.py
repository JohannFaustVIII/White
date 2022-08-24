import random

from tensorflow.keras.models import Sequential

from Map import Map
from Player import Player

class NNPlayer(Player):

    def __init__(self, model: Sequential, discover : float) -> None:
        super().__init__()
        self.model = model
        self.discover = discover

    def get_move(self, map : Map, first_player : bool) -> int:
        moves = map.get_possible_moves()
        print(moves)
        if random.random() < self.discover:
            return random.choice(moves)
        else:
            valued_moves = [(move, self.model.preditct(map.get_points_for_move(move, first_player))) for move in moves]
            max_move = max(valued_moves, key=lambda x: x[1])
            return max_move[0]
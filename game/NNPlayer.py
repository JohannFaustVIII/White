import random
import tensorflow as tf

from Map import Map
from Player import Player

class NNPlayer(Player):

    def __init__(self, model, discover : float, verbose : bool = False, extra_verbose : bool = False) -> None:
        super().__init__()
        self.model = model
        self.discover = discover
        self.verbose = verbose
        self.extra_verbose = extra_verbose

    def get_move(self, map : Map, first_player : bool) -> int:
        moves = map.get_possible_moves(first_player)
        if random.random() < self.discover:
            move = random.choice(moves)
        else:
            def predict_func(move):
                value = self.model.predict([map.get_points_for_move(move, first_player)], verbose = 0)
                if self.extra_verbose:
                    print(f"Move {move} value = {value}")
                return (move, value) 
            valued_moves = [predict_func(move) for move in moves]
            max_move = max(valued_moves, key=lambda x: x[1])
            move = max_move[0]
        if self.verbose:
            print(f"Chosen move is: {move}")
        return move
import random
import tensorflow as tf

from Map import Map
from Player import Player

class NNPlayer(Player):

    predict_memory = {}

    def __init__(self, model, discover : float, verbose : bool = False, extra_verbose : bool = False) -> None:
        super().__init__()
        self.model = model
        self.discover = discover
        self.verbose = verbose
        self.extra_verbose = extra_verbose

    def get_move(self, map : Map, first_player : bool, use_memory : bool = True) -> int:
        moves = map.get_possible_moves(first_player)
        if random.random() < self.discover:
            move = random.choice(moves)
        else:
            def predict_func(move):
                state = map.get_points_for_move(move, first_player)
                if use_memory:
                    value = NNPlayer.predict(self.model, state)
                else:
                    value = self.model.predict([state], verbose = 0)
                if self.extra_verbose:
                    print(f"Move {move} value = {value}")
                return (move, value) 
            valued_moves = [predict_func(move) for move in moves]
            max_move = max(valued_moves, key=lambda x: x[1])
            move = max_move[0]
        self.__print_move(move)
        return move
    
    def __print_move(self, move : int) :
        if self.verbose:
            print(f"\nNNPlayer chosen move is {move}\n")

    def clean_memory() :
        NNPlayer.predict_memory = {}
    
    def predict(model, state : list[list[int]]) -> int:
        mid_k = [tuple(s) for s in state]
        k = tuple(mid_k)
        if k not in NNPlayer.predict_memory:
            value = model.predict([state], verbose = 0)
            NNPlayer.predict_memory[k] = value
            return value
        else:
            return NNPlayer.predict_memory[k]
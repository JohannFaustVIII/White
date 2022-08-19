from Map import Map
from Player import Player

class NNPlayer(Player):

    def __init__(self) -> None:
        super().__init__()
        # player's parameters have to be set from the outside
        # 1. here to provide NN and check its parameters? or load here? first option looks better
        # 2. add setting flag to register moves (training to be done outside) <- that requires a list of end positions of this player
        # 3. pass discover parameter to enable discovering new moves

    def get_move(self, map : Map) -> int:
        # if random less than discover:
        #   get available moves
        #   choose random of them
        #   save state after move ??? <- is it required? if move will be returned outside, then state after move can be saved there?
        #   return move
        # else:
        #   get available move
        #   for each available move:
        #       get state of map after move
        #       get state prediction from NN (value between 0 to 1, 0 - state lost, 1 - state win)
        #       decide about maximum <- the closest to win
        #   save state after move ??? <- again to think
        #   return move making a state the closest to a win
        pass
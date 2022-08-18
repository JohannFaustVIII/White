from Map import Map
from Player import Player

class NNPlayer(Player):

    def __init__(self) -> None:
        super().__init__()
        # player's parameters have to be set from the outside
        # 1. here to provide NN and check its parameters? or load here? first option looks better
        # 2. add setting flag to register moves (training to be done outside) <- that requires a separate class for move win/lose count
        # 3. pass discover parameter to enable discovering new moves

    def get_move(self, map : Map) -> int:
        #TODO : to implement, more like to be implemented by extending classes
        pass
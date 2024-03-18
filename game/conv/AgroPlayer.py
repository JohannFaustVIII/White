from ABPlayer import ABPlayer

class AgroPlayer(ABPlayer):
    
    moves_memory = {}

    def __init__(self, depth : int = 1, verbose : bool = False, use_memory : bool = False) -> None:
        super().__init__(depth, verbose, use_memory)

        self.__depth = depth
    
    def compute_distance(self, depth, first_player, map):
        side_to_compute = first_player if (self.__depth - depth) % 2 == 0 else not first_player

        dist_map = map.get_distance_map()

        compare_function = min if side_to_compute else max

        gate_y = compare_function([k[1] for k in dist_map.keys()])

        keys = [k for k in dist_map.keys() if k[1] == gate_y]

        _min_dist = min([dist_map[k] for k in keys])
        move_value = -1 * _min_dist

        return move_value
    
    def get_from_memory(self, state):
        if state in AgroPlayer.moves_memory:
            return AgroPlayer.moves_memory[state]
        else:
            return None
    
    def put_in_memory(self, state, value):
        AgroPlayer.moves_memory[state] = value

    def get_memory_size(self):
        return len(AgroPlayer.moves_memory)
    
    def get_name(self) -> str:
        return "AgroPlayer"
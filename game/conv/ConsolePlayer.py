from Map import Map
from Player import Player

class ConsolePlayer(Player):
    
    def __init__(self, name : str = "") -> None:
        super().__init__()
        self.name = name

    def get_move(self, map : Map, first_player : bool) -> int:
        move = -1
        possible_moves = map.get_possible_moves(first_player)
        print(self.name)
        while move not in possible_moves:
            move = int(input(f"\nPossible moves: {possible_moves}\nPlease, enter a move: "))
            if move not in possible_moves:
                print("Provided move is not possible!!!")
        return move
    
    def get_name(self) -> str:
        return "ConsolePlayer"
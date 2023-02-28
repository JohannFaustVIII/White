from Map import Map
from Player import Player

class ConsolePlayer(Player):
    
    def get_move(self, map : Map, first_player : bool) -> int:
        move = -1
        possible_moves = map.get_possible_moves(first_player)
        while move not in possible_moves:
            move = int(input(f"Possible moves: {possible_moves}\nPlease, enter a move: "))
            if move not in possible_moves:
                print("Provided move is not possible")
        return move
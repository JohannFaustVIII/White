from Map import Map
from Player import Player

class ConsolePlayer(Player):
    
    def __init__(self, name : str = "", show_map : bool = False) -> None:
        super().__init__()
        self.name = name
        self.__show_map = show_map

    def get_move(self, map : Map, first_player : bool) -> int:
        move = -1
        if self.__show_map:
            self.print_map(map, first_player)
        possible_moves = map.get_possible_moves(first_player)
        print(self.name)
        while move not in possible_moves:
            move = int(input(f"\nPossible moves: {possible_moves}\nPlease, enter a move: "))
            if move not in possible_moves:
                print("Provided move is not possible!!!")
        return move
    
    def get_name(self) -> str:
        return "ConsolePlayer"
    
    def print_map(self, map, first_player):
        counter = 0
        mid_counter = 0

        true_map = [
            ["\\", "|", "/"],
            ["-", "0", "-"],
            ["/", "|", "\\"]
        ]

        false_map = [
            [" ", " ", " "],
            [" ", ".", " "],
            [" ", " ", " "]
        ]

        start_map = map.get_points(first_player)

        for p in start_map:

            line = ""

            for v in p:
                line += true_map[counter][mid_counter] if bool(v) else false_map[counter][mid_counter]
                mid_counter = (mid_counter + 1) % 3

            counter = (counter + 1) % 3
            print(line)
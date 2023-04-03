class Point:

    def __init__(self):
        self.lines = [False for i in range(8)]

    def do_move(self, move : int, value : bool):
        if (move < 0 or move > 7):
            raise ValueError('Wrong move!')
        self.lines[move] = value
    
    def get_move(self, move : int) -> bool:
        return self.lines[move]
    
    def mark_moves(self, moves : list[int]):
        for move in moves:
            self.lines[move] = True

    def get_as_conv(self) -> list[list[int]]:
        return [
            [int(self.lines[7]), int(self.lines[0]), int(self.lines[1])],
            [int(self.lines[6]), 0, int(self.lines[2])],
            [int(self.lines[5]), int(self.lines[4]), int(self.lines[3])]
        ]
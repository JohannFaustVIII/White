class Point:

    def __init__(self):
        self.lines = [False for i in range(8)]

    def do_move(self, move : int, value : bool):
        if (move < 0 or move > 7):
            raise ValueError('Wrong move!')
        self.lines[move] = value
    
    def get_move(self, move : int) -> bool:
        return self.lines[move]
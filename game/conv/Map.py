from Point import Point

class Map:
    
    __second_player_moves = [4, 5, 6, 7, 0, 1, 2, 3]

    def __init__(self, width : int, height : int) -> None:
        self.__width = width
        self.__height = height
        self.__position_x = int(width/2)
        self.__position_y = int(height/2)
        self.__points = Map.__generate_points(width, height)
    
    def get_points(self, first_player) -> list[list[int]]:
        result = [point.get_as_conv() for point in self.__points]
        result[self.__get_current_point_index()][1][1] = 1
        line_map = []
        for x in range(0, len(result), self.__width + 1):
            top = []
            middle = []
            bottom = []

            for p in result[x:x + (self.__width + 1)]:
                top.extend(p[0])
                middle.extend(p[1])
                bottom.extend(p[2])

            line_map.append(top)
            line_map.append(middle)
            line_map.append(bottom)

        if not first_player:
            for p in line_map:
                p.reverse()
            line_map.reverse()

        return line_map

    def get_points_for_move(self, move : int, first_player : bool) -> list[list[int]]:
        self.make_move(move, first_player)
        result = self.get_points(first_player)
        self.revert_move(move, first_player)
        return result

    def make_move(self, move : int, first_player : bool = True) -> None:
        if not first_player:
            move = Map.__second_player_moves[move]
        self.__update_point(move, True)
        self.__make_move(move)
        self.__update_point((move + 4) % 8, True)

    def revert_move(self, move : int, first_player : bool) -> None:
        if not first_player:
            move = Map.__second_player_moves[move]
        self.__update_point((move + 4) % 8, False)
        self.__make_move((move + 4) % 8)
        self.__update_point(move, False)

    def __update_point(self, move : int, value : bool) -> None:
        index = self.__get_current_point_index()
        point = self.__points[index]
        point.do_move(move, value)

    def __get_current_point_index(self) -> int:
        return (self.__position_y + 1) * (self.__width + 1) + self.__position_x

    def __make_move(self, move : int) -> None:
        left_moves = [1, 2, 3]
        right_moves = [5, 6, 7]
        up_moves = [7, 0, 1]
        down_moves = [3, 4, 5]

        if move in left_moves:
            self.__position_x += 1
        elif move in right_moves:
            self.__position_x -= 1

        if move in up_moves:
            self.__position_y -= 1
        elif move in down_moves:
            self.__position_y += 1

    def is_end_of_game(self) -> bool:
        return self.is_goal(True) or self.is_goal(False) or not self.get_possible_moves()
    
    def get_possible_moves(self, is_first_player: bool = True) -> list[int]:
        possible = [x for x in range(0, 8) if self.is_move_possible(x)]
        if not is_first_player:
            possible = [Map.__second_player_moves[move] for move in possible]
            possible.sort()
        return possible

    def is_move_possible(self, move : int) -> bool:
        if self.__position_y == -1 or self.__position_y == self.__height + 1 :
            return True
        return not self.__points[self.__get_current_point_index()].get_move(move)

    def is_continuous_move_possible(self) -> bool:
        if self.__position_y in [-1, self.__height + 1]:
            return False
        point = self.__points[self.__get_current_point_index()]
        counter = sum(point.lines)

        return counter > 1

    def is_goal(self, first_player : bool) -> bool:
        if first_player:
            return self.__position_y == -1
        else:
            return self.__position_y == self.__height + 1
        
    def __generate_points(width : int, height : int) -> list[Point]:
        points = []

        # first line

        for _ in range(int((width-2)/2)):
            point = Point()
            point.mark_moves([0, 1, 2, 3, 4, 5, 6, 7])
            points.append(point)
    
        left = Point()
        left.mark_moves([0, 1, 2, 4, 5, 6, 7])
        points.append(left)

        middle = Point()
        middle.mark_moves([0, 1, 2, 6, 7])
        points.append(middle)

        right = Point()
        right.mark_moves([0, 1, 2, 3, 4, 6, 7])
        points.append(right)

        for _ in range(int((width-2)/2)):
            point = Point()
            point.mark_moves([0, 1, 2, 3, 4, 5, 6, 7])
            points.append(point)

        # second line 

        left_corner = Point()
        left_corner.mark_moves([0, 1, 2, 4, 5, 6, 7])
        points.append(left_corner)

        for _ in range(int((width-4)/2)):
            point = Point()
            point.mark_moves([0, 1, 2, 6, 7])
            points.append(point)

        left = Point()
        left.mark_moves([0, 6, 7])
        points.append(left)

        points.append(Point())

        right = Point()
        right.mark_moves([0, 1, 2])
        points.append(right)

        for _ in range(int((width-4)/2)):
            point = Point()
            point.mark_moves([0, 1, 2, 6, 7])
            points.append(point)

        right_corner = Point()
        right_corner.mark_moves([0, 1, 2, 3, 4, 6, 7])
        points.append(right_corner)

        # middle lines

        for _ in range(height - 1):
            
            left = Point()
            left.mark_moves([0, 4, 5, 6, 7])
            points.append(left)

            for _ in range(width - 1):
                points.append(Point())

            right = Point()
            right.mark_moves([0, 1, 2, 3, 4])
            points.append(right)

        # pre last line

        left_corner = Point()
        left_corner.mark_moves([0, 2, 3, 4, 5, 6, 7])
        points.append(left_corner)

        for _ in range(int((width-4)/2)):
            point = Point()
            point.mark_moves([2, 3, 4, 5, 6])
            points.append(point)

        left = Point()
        left.mark_moves([4, 5, 6])
        points.append(left)

        points.append(Point())

        right = Point()
        right.mark_moves([2, 3, 4])
        points.append(right)

        for _ in range(int((width-4)/2)):
            point = Point()
            point.mark_moves([2, 3, 4, 5, 6])
            points.append(point)

        right_corner = Point()
        right_corner.mark_moves([0, 1, 2, 3, 4, 5, 6])
        points.append(right_corner)

        # last line

        for _ in range(int((width-2)/2)):
            point = Point()
            point.mark_moves([0, 1, 2, 3, 4, 5, 6, 7])
            points.append(point)
    
        left = Point()
        left.mark_moves([0, 2, 3, 4, 5, 6, 7])
        points.append(left)

        middle = Point()
        middle.mark_moves([2, 3, 4, 5, 6])
        points.append(middle)

        right = Point()
        right.mark_moves([0, 1, 2, 3, 4, 5, 6])
        points.append(right)

        for _ in range(int((width-2)/2)):
            point = Point()
            point.mark_moves([0, 1, 2, 3, 4, 5, 6, 7])
            points.append(point)

        return points
    
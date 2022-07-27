from Point import Point

class Map:

    def __init__(self, width : int, height : int) -> None:
        self.__width = width
        self.__height = height
        self.__position_x = int(width/2)
        self.__position_y = int(height/2)
        self.__points = [Point() for i in range(0, 6 + (width + 1) * (height + 1))]

    def make_move(self, move : int) -> None:
        self.__update_point(move)
        self.__make_move(move)
        self.__update_point((move + 4) % 8)
        pass
    
    def __update_point(self, move : int) -> None:
        index = self.__get_current_point_index()
        point = self.__points[index]
        point.do_move(move)

    def __make_move(self, move : int) -> None:
        left_moves = [1, 2, 3]
        right_moves = [5, 6, 7]
        up_moves = [7, 0 ,1]
        down_moves = [3, 4, 5]

        if move in left_moves:
            self.__position_x += 1
        elif move in right_moves:
            self.__position_x -= 1

        if move in up_moves:
            self.__position_y -= 1
        elif move in down_moves:
            self.__position_y += 1

    def is_continuous_move_possible(self) -> bool:
        if self.__position_y in [-1, self.__height + 1]:
            return False
        point = self.__points[self.__get_current_point_index()]
        counter = sum(point.lines)

        if self.__position_x in [0, self.__width]:
            if counter == 3:
                return False
            elif self.__position_y in [0, self.__height]:
                return False
            else:
                return True
        
        if self.__position_y in [0, self.__height]:
            if self.__position_x < (self.__width/2 - 1) or self.__position_x > (self.__width/2 + 1):
                if counter == 3:
                    return False
                else:
                    return True
            else:
                if self.__position_x != self.__width/2:
                    if counter == 5:
                        return False
                    else:
                        return True
        
        return counter > 1

    def __get_current_point_index(self) -> int:
        if self.__position_y == -1:
            index = self.__position_x - int(self.__width / 2) + 1
        elif self.__position_y == self.__height + 1:
            index = len(self.__points) - 3 + self.__position_x - int(self.__width / 2) + 1
        else:
            index = 3 + (self.__width + 1) * self.__position_y + self.__position_x
        return index
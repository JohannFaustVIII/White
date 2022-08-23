from collections import deque
from itertools import chain
from Point import Point

class Map:

    __second_player_moves = [4, 5, 6, 7, 0, 1, 2, 3]

    def __init__(self, width : int, height : int) -> None:
        self.__width = width
        self.__height = height
        self.__position_x = int(width/2)
        self.__position_y = int(height/2)
        self.__points = [Point() for i in range(0, 6 + (width + 1) * (height + 1))]

    def get_points_for_move(self, move : int, first_player : bool) -> list[int]:
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

    def is_end_of_game(self) -> bool:
        return self.is_goal(True) or self.is_goal(False) or not self.get_possible_moves()

    def is_enemy_goal(self, first_player : bool) -> None:
        return self.is_goal(not first_player)

    def is_goal(self, first_player : bool) -> None:
        if first_player:
            return self.__position_y == -1
        else:
            return self.__position_y == self.__height + 1
    
    def __update_point(self, move : int, value : bool) -> None:
        index = self.__get_current_point_index()
        point = self.__points[index]
        point.do_move(move, value)

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

    def get_possible_moves(self) -> list[int]:
        return [x for x in range(0, 8) if self.is_move_possible(x)]

    def is_move_possible(self, move : int) -> bool:
        if self.__position_y == -1 or self.__position_y == self.__height + 1 :
            return True
        match move:
            case 0:
                if self.__position_x in [0, self.__width]:
                    return False
                if self.__position_y == 0 and self.__position_x != int(self.__width/2):
                    return False
                pass
            case 1:
                if self.__position_x == self.__width:
                    return False
                if self.__position_y == 0 and self.__position_x not in [int(self.__width/2), int(self.__width/2)-1]:
                    return False
                pass
            case 2:
                if self.__position_x == self.__width:
                    return False
                if self.__position_y in [0, self.__height] and self.__position_x not in [int(self.__width/2), int(self.__width/2)-1]:
                    return False
                pass
            case 3:
                if self.__position_x == self.__width:
                    return False
                if self.__position_y == self.__height and self.__position_x not in [int(self.__width/2), int(self.__width/2)-1]:
                    return False
                pass
            case 4:
                if self.__position_x in [0, self.__width]:
                    return False
                if self.__position_y == self.__height and self.__position_x != int(self.__width/2):
                    return False
                pass
            case 5:
                if self.__position_x == 0:
                    return False
                if self.__position_y == self.__height and self.__position_x not in [int(self.__width/2), int(self.__width/2)+1]:
                    return False
                pass
            case 6:
                if self.__position_x == 0:
                    return False
                if self.__position_y in [0, self.__height] and self.__position_x not in [int(self.__width/2), int(self.__width/2)+1]:
                    return False
                pass
            case 7:
                if self.__position_x == 0:
                    return False
                if self.__position_y == 0 and self.__position_x not in [int(self.__width/2), int(self.__width/2)+1]:
                    return False
                pass
        return not self.__points[self.__get_current_point_index()].get_move(move)

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

    def get_points(self, first_player) -> list[int]:
        if first_player:
            result = [Map.__bool_to_int_list(x.lines) for x in self.__points]
        else:
            result = [Map.__bool_to_int_list(Map.__rotate_list_for_second_player(x.lines)) for x in self.__points]
            result.reverse()
        return Map.__merge_lists_into_single_list(result)
    
    def __bool_to_int_list(list : list[bool]) -> list[int]:
        return [int(x) for x in list]

    def __rotate_list_for_second_player(list_to_rotate : list[bool]) -> list[bool]:
        d = deque(list_to_rotate)
        d.rotate(4)
        return list(d)

    def __merge_lists_into_single_list(lists : list[list[int]]) -> list[int]:
        return list(chain.from_iterable(lists))
from turtle import width
from Point import Point

class Map:

    __second_player_moves = [4, 5, 6, 7, 0, 1, 2, 3]

    def __init__(self, width : int, height : int) -> None:
        self.__width = width
        self.__height = height
        self.__position_x = int(width/2)
        self.__position_y = int(height/2)
        self.__points = [Point() for i in range(0, 6 + (width + 1) * (height + 1))]

    def make_move(self, move : int, first_player : bool) -> None:
        if bool == True:
            self.make_move(move)
        else:
            self.make_move(Map.__second_player_moves[move])

    def make_move(self, move : int) -> None:
        self.__update_point(move, True)
        self.__make_move(move)
        self.__update_point((move + 4) % 8, True)
    
    def revert_move(self, move : int, first_player : bool) -> None:
        if first_player:
            self.revert_move(move)
        else:
            self.revert_move(Map.__second_player_moves[move])

    def revert_move(self, move : int) -> None:
        self.__update_point((move + 4) % 8, False)
        self.__make_move((move + 4) % 8)
        self.__update_point(move, False)

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
        return not self.__points[self.__get_current_point_index].get_move(move)


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

    def get_map_as_list(self, first_player : bool) -> list[int]:
        if (first_player):
            goal_points = self.__points[3 + int(self.__width/2) - 1: 3 + int(self.__width/2) + 2]
            enemy_goal = [x.get_move(1) for x in goal_points[0:-1]] + [x.get_move(0) for x in goal_points[1:-1]] + [x.get_move(7) for x in goal_points[1:]] + [x.get_move(2) for x in goal_points[0:-1]]
            middle_points = []
            for i in range(0, self.__height):
                shift_index = 3 + (self.__width + 1) * i
                points = self.__points[shift_index : shift_index + self.__width + 1]
                middle_points += [x.get_move(1) for x in points[0:-1]]
                middle_points += [x.get_move(0) for x in points[1:-1]]
                middle_points += [x.get_move(7) for x in points[1:]]
                if (i != self.__height - 1):
                    middle_points += [x.get_move(2) for x in points[0:-1]]
            my_goal_shift = len(self.__points) - (3 + int(self.__width/2) + 1) - 1
            my_goal_points = self.__points[my_goal_shift: my_goal_shift + 2]
            my_goal = [x.get_move(2) for x in my_goal_points[0:-1]] + [x.get_move(5) for x in my_goal_points[1:]] + [x.get_move(4) for x in my_goal_points[1:-1]] + [x.get_move(3) for x in my_goal_points[0:-1]]
            return enemy_goal + middle_points + my_goal
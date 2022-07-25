from Point import Point

class Map:

    def __init__(self, width : int, height : int) -> None:
        self.__width = width
        self.__height = height
        self.__position_x = width/2
        self.__position_y = height/2
        self.__points = [Point() for i in range(0, 6 + (width + 1) * (height + 1))]
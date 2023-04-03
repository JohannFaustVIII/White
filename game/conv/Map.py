from Point import Point

class Map:
    
    def __init__(self, width : int, height : int) -> None:
        self.__width = width
        self.__height = height
        self.__position_x = int(width/2)
        self.__position_y = int(height/2)
        self.__points = Map.__generate_points(width, height)

    def get_points(self):
        return self.__points

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
    

from enum import Enum

from point import Point


class Axis(Enum):
    X = 1
    Y = 2


class SimpleLine:

    def __init__(self, p0, direction, length):
        self.p0 = p0
        self.length = length
        if direction == "U":
            self.axis = Axis.X
            self.value = p0.x
            self.min = p0.y
            self.max = p0.y + length
            self.p1 = Point(p0.x, p0.y + length)
        elif direction == "D":
            self.axis = Axis.X
            self.value = p0.x
            self.min = p0.y - length
            self.max = p0.y
            self.p1 = Point(p0.x, p0.y - length)
        elif direction == "R":
            self.axis = Axis.Y
            self.value = p0.y
            self.min = p0.x
            self.max = p0.x + length
            self.p1 = Point(p0.x + length, p0.y)
        elif direction == "L":
            self.axis = Axis.Y
            self.value = p0.y
            self.min = p0.x - length
            self.max = p0.x
            self.p1 = Point(p0.x - length, p0.y)
        else:
            raise Exception("The direction %s is not a valid value" % direction)


def get_intersection(line1, line2):
    if line1.axis == line2.axis:
        return None

    x = line1.value if line1.axis == Axis.X else line2.value
    y = line1.value if line1.axis == Axis.Y else line2.value
    if point_on_section(line1, Point(x, y)) and point_on_section(line2, Point(x, y)):
        return Point(x, y)

    return None


def point_on_section(line, point):
    if line.axis == Axis.X:
        return line.value == point.x and line.min <= point.y <= line.max
    else:
        return line.value == point.y and line.min <= point.x <= line.max

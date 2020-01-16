from enum import Enum


class Direction(Enum):
    SOUTH = (2, 3, (1, 0))
    NORTH = (1, 1, (-1, 0))
    EAST = (3, 2, (0, 1))
    WEST = (4, 4, (0, -1))

    def __init__(self, input_code, direction, twod_direction):
        self.input_code = input_code
        self.direction = direction
        self.twod_direction = twod_direction

    @staticmethod
    def from_direction(value):
        for direction in Direction:
            if direction.direction == value:
                return direction
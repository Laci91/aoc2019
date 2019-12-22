import logging
from enum import Enum

import file_utils
from intcode_interpreter import IntcodeInterpreter

logging.basicConfig()


class Direction(Enum):
    NORTH = (1, 1, (0, 1))
    SOUTH = (2, 3, (0, -1))
    EAST = (3, 2, (1, 0))
    WEST = (4, 4, (-1, 0))

    def __init__(self, input_code, direction, twod_direction):
        self.input_code = input_code
        self.direction = direction
        self.twod_direction = twod_direction

    @staticmethod
    def from_direction(value):
        for direction in Direction:
            if direction.direction == value:
                return direction

        raise Exception('No such value in Direction enum: %s' % value)


def calculate_direction(output, direction):
    if output == 1:
        return Direction.from_direction(direction.direction % 4 + 1)
    elif output == 0:
        return Direction.from_direction((direction.direction - 2) % 4 + 1)
    else:
        raise Exception('Invalid output received')


def oxygen_tracker(robot, position, previous_movement, current_time):
    local_max = current_time
    for direction in Direction:
        if previous_movement[0] * -1 == direction.twod_direction[0] and previous_movement[1] * -1 == direction.twod_direction[1]:
            continue

        new_robot = IntcodeInterpreter.from_computer(robot)
        new_robot.set_inputs([direction.input_code])
        while new_robot.process_next_code():
            pass

        outputs = new_robot.get_outputs()
        if outputs[0] == 1:
            new_position = (position[0] + direction.twod_direction[0], position[1] + direction.twod_direction[1])
            output = oxygen_tracker(new_robot, new_position, direction.twod_direction, current_time + 1)
            if output > local_max:
                local_max = output

    return local_max


if __name__ == "__main__":
    instructions = file_utils.read_comma_delimited_ints("input15.txt")
    robot = IntcodeInterpreter(instructions, [])

    last_output = 1
    direction = Direction.NORTH
    pos = (0, 0)
    while not robot.finished:
        print("Moving %s" % direction)
        direction = calculate_direction(last_output, direction)
        robot.set_inputs([direction.input_code])
        while robot.process_next_code():
            pass

        last_output = robot.get_outputs()[0]
        if last_output == 0:
            pos = (pos[0] + direction.twod_direction[0], pos[1] + direction.twod_direction[1])
        if last_output == 2:
            print("Found the oxygen tank, starting backtracking")
            break

    max_time = oxygen_tracker(robot, pos, (0, 0), 0)
    print(max_time)

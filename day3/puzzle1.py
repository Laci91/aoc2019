import file_utils
import simple_line
from point import Point
from simple_line import SimpleLine


def execute_step(starting_point, direction, step_count):
    return SimpleLine(starting_point, direction, step_count)


def get_all_lines(wire_directions):
    wire_data_points = list()
    current_point = Point(0, 0)

    wire_directions_list = wire_directions.split(",")
    for direction in wire_directions_list:
        line = SimpleLine(current_point, direction[0], int(direction[1:]))
        current_point = line.p1
        wire_data_points.append(line)

    return wire_data_points


if __name__ == "__main__":
    wires = file_utils.read_lines("input03.txt")
    wire1 = get_all_lines(wires[0])
    wire2 = get_all_lines(wires[1])

    intersections = filter(None, [simple_line.get_intersection(p1, p2) for p1 in wire1 for p2 in wire2])
    print("Calculated intersections")
    print(min([abs(a) + abs(b) for a, b in intersections if a != 0 or b != 0]))

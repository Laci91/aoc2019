import day3.puzzle1
import file_utils
import simple_line
from point import Point


def get_points_on_line(line, points):
    return filter(lambda p: simple_line.point_on_section(line, p), points)


def get_residual_distance(line, point):
    return abs(line.p0.y - point.y) if line.axis == simple_line.Axis.X else abs(line.p0.x - point.x)


def calculate_steps_for_points(wire, control_points):
    step_count = 0
    control_point_map = {}
    for line in wire:
        points = get_points_on_line(line, control_points)
        for point in points:
            residual_distance = get_residual_distance(line, point)
            control_point_map[point] = step_count + residual_distance

        step_count += line.length

    return control_point_map


if __name__ == "__main__":
    wires = file_utils.read_lines("input03.txt")
    wire1 = day3.puzzle1.get_all_lines(wires[0])
    wire2 = day3.puzzle1.get_all_lines(wires[1])

    intersections = list(filter(None, [simple_line.get_intersection(l1, l2) for l1 in wire1 for l2 in wire2]))
    nonzero_intersecting_points = [point for point in intersections if point != Point(0, 0)]

    wire1_map = calculate_steps_for_points(wire1, nonzero_intersecting_points)
    wire2_map = calculate_steps_for_points(wire2, nonzero_intersecting_points)

    print(min([wire1_map[point] + wire2_map[point] for point in nonzero_intersecting_points]))

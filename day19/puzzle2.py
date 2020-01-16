import math

from intcode_interpreter import IntcodeInterpreter


def find_line_gradient(points, check_passed):
    recommended_point = None

    for x, y in points:
        if not recommended_point:
            print("Setting point to (%d, %d)" % (x, y))
            recommended_point = (x, y)
        elif check_passed(recommended_point[1]*x - recommended_point[0]*y, 0):
            print("New recommended point: (%d, %d)" % (x, y))
            recommended_point = (x, y)

    return recommended_point


if __name__ == "__main__":
    base_computer = IntcodeInterpreter.from_file("input19.txt")
    inputs = []
    for x in range(0, 50):
        for y in range(0, 50):
            inputs += [[x, y]]

    beam_cover = []
    for i in inputs:
        computer = IntcodeInterpreter.from_computer(base_computer)
        computer.set_inputs(i)
        while computer.process_next_code():
            pass

        output = computer.get_outputs()[0]
        if output == 1:
            beam_cover += [(i[0], i[1])]

    print(beam_cover)

    grouped_beam_cover = [[(x, y) for x, y in beam_cover if x == n] for n in range(1, 50)]
    print(grouped_beam_cover)

    lower_bound = [sorted(l, key=lambda a: a[1])[0] for l in grouped_beam_cover if l != []]
    upper_bound = [sorted(l, key=lambda a: a[1], reverse=True)[0] for l in grouped_beam_cover if l != []]

    print("Find lower bound")
    boundary_point_down = find_line_gradient(lower_bound, lambda a, b: a < b)
    print("Find upper bound")
    boundary_point_up = find_line_gradient(upper_bound, lambda a, b: a > b)

    a = boundary_point_down[0]
    b = boundary_point_down[1]
    c = boundary_point_up[0]
    d = boundary_point_up[1]

    x = 0
    while True:
        y = math.floor(b/a*x)
        dx = x + 100
        dy = y - 100
        print("(%d, %d) -> (%d, %d) wanted, actual point is (%d, %d)" % (x, y, dx, dy, dx, math.floor(d/c*dx)))
        if math.floor(d/c*dx) == dy:
            print("Success")
            break
        x += 1

    print(str(x * 10000 + dy))






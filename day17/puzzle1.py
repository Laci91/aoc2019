import logging

from intcode_interpreter import IntcodeInterpreter

logging.basicConfig(level=logging.INFO)


def is_intersection(x, y, map):
    print("(%d, %d)" % (x, y))
    if map[x][y] != "#":
        return False
    if x != 0 and map[x-1][y] != "#":
        return False
    if x != len(map) - 1 and map[x+1][y] != "#":
        return False
    if y != 0 and map[x][y-1] != "#":
        return False
    if y != len(map[0]) - 1 and map[x][y+1] != "#":
        return False
    return True


if __name__ == "__main__":
    robot = IntcodeInterpreter.from_file("input17.txt")
    while not robot.finished:
        while robot.process_next_code():
            pass

    output = robot.get_outputs()
    mapStr = "".join([chr(o) for o in output])
    map = [line for line in mapStr.split("\n") if line != ""]
    print(map)
    new_map = []
    alignment_parameters = 0
    for i in range(0, len(map)):
        new_map.append([])
        for j in range(0, len(map[i])):
            if is_intersection(i, j, map):
                new_map[i].append("O")
                alignment_parameters += i*j
            else:
                new_map[i].append(map[i][j])

    print("\n".join(["".join(line) for line in new_map]))
    print(alignment_parameters)

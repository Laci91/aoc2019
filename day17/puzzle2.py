import logging

from direction import Direction
from intcode_interpreter import IntcodeInterpreter

logging.basicConfig(level=logging.INFO)


def find_robot(map):
    for i in range(0, len(map)):
        for j in range(0, len(map[i])):
            if map[i][j] == "^":
                return i, j


def get_new_position(pos, direction):
    return pos[0] + direction.twod_direction[0], pos[1] + direction.twod_direction[1]


def get_value_in_position(pos, map):
    return map[pos[0]][pos[1]]


def is_inside_bounds(pos, min_x, max_x, min_y, max_y):
    return min_x <= pos[0] <= max_x and min_y <= pos[1] <= max_y


def turn(position, direction, map):
    # Try turning right
    right = Direction.from_direction((direction.direction % 4) + 1)
    left = Direction.from_direction(((direction.direction - 2) % 4 + 1))
    for i in [("R", right), ("L", left)]:
        proposed_position = get_new_position(position, i[1])
        if not is_inside_bounds(proposed_position, 0, len(map) - 1, 0, len(map[0]) - 1):
            continue

        if get_value_in_position(proposed_position, map) == "#":
            return i[0], i[1]


def navigate_robot(map, position):
    direction = Direction.NORTH
    instructions = []
    step_count = 0
    while True:
        proposed_position = get_new_position(position, direction)
        if not is_inside_bounds(proposed_position, 0, len(map) - 1, 0, len(map[0]) - 1):
            instructions.append(step_count)
            step_count = 0
            turn_instructions = turn(position, direction, map)
            if turn_instructions is None:
                break
            instructions.append(turn_instructions[0])
            direction = turn_instructions[1]
        elif map[proposed_position[0]][proposed_position[1]] != "#":
            instructions.append(step_count)
            step_count = 0
            turn_instructions = turn(position, direction, map)
            if turn_instructions is None:
                break
            instructions.append(turn_instructions[0])
            direction = turn_instructions[1]
        else:
            position = proposed_position
            step_count += 1

    return instructions


def replace_occurrence_with_x(plan, sublist):
    for i in range(0, len(plan) - len(sublist) + 1):
        if plan[i:i+len(sublist)] == sublist:
            plan = plan[0:i] + ["X"]*len(sublist) + plan[i+len(sublist):]

    return plan


def find_movement_details(plan, movement_details):
    if len(movement_details) == 3 and [s for s in plan if s != "X"] != []:
        # print("Voting for %s as failed because of leftover pieces" % movement_details)
        print(plan, movement_details)
        return None
    elif len(movement_details) == 3 and plan == [] and sum([len(l) for l in movement_details]) > 20:
        # print("Voting for %s as failed because of memory overflow" % movement_details)
        return None
    elif len(movement_details) == 3:
        print(plan, movement_details)
        return movement_details

    for i in range(2, min(16, len(plan))):
        first_nonx = min([item for item in range(0, len(plan)) if plan[item] != "X"])
        new_detail = plan[first_nonx:i+first_nonx]
        if "X" in new_detail:
            return None
        new_plan = replace_occurrence_with_x(plan, new_detail)
        output = find_movement_details(new_plan, movement_details + [new_detail])
        if output:
            return output


def generate_routines_from_instructions_set(plan, subroutines):
    subroutine_list = list(subroutines)
    routines = []
    while len(plan) > 0:
        for name, subroutine in subroutine_list:
            if plan[0:len(subroutine)] == subroutine:
                routines += [name]
                plan = plan[len(subroutine):]

    return routines


if __name__ == "__main__":
    robot = IntcodeInterpreter.from_file("input17.txt")
    while not robot.finished:
        while robot.process_next_code():
            pass

    output = robot.get_outputs()
    mapStr = "".join([chr(o) for o in output])
    map = [line for line in mapStr.split("\n") if line != ""]
    print("\n".join(map))

    pos = find_robot(map)
    plan = navigate_robot(map, pos)[1:]
    joined_plan = ["".join([str(j) for j in plan[i:i+2]]) for i in range(0, len(plan), 2)]

    movement_details = find_movement_details(joined_plan, [])
    joined_instructions = [",".join([str[0:1] + "," + str[1:] for str in l]) for l in movement_details]
    print(joined_instructions)
    routines = generate_routines_from_instructions_set(joined_plan, zip("ABC", movement_details))
    joined_routines = ",".join(routines)
    print(joined_routines)
    pre_input = [[ord(c) for c in joined_routines]] + [[ord(c) for c in instr] for instr in joined_instructions]
    print(pre_input)
    final_input = pre_input[0] + [10] + pre_input[1] + [10] + pre_input[2] + [10] + pre_input[3] + [10, ord("y"), 10]

    robot = IntcodeInterpreter.from_file("input17.txt")
    robot.memory[0] = 2
    robot.set_inputs(final_input)
    while robot.process_next_code():
        pass

    print(robot.finished, robot.waiting_for_input, robot.get_outputs())



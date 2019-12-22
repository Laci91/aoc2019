import logging

import file_utils
from intcode_interpreter import IntcodeInterpreter
from point import Point

logging.basicConfig(level=logging.INFO)


class Field:
    def __init__(self, place, color, num_visited):
        self.place = place
        self.color = color
        self.num_visited = num_visited

    def __repr__(self):
        return "Place: (%d, %d); Color: %d; Visited: %d" % (self.place.x, self.place.y, self.color, self.num_visited)

    def visit(self, new_color):
        self.color = new_color
        self.num_visited += 1


def find_field(fields, position):
    return fields[position] if position in fields else Field(pos, 0, 0)


if __name__ == "__main__":
    memory = file_utils.read_comma_delimited_ints("test.txt")
    instructions = IntcodeInterpreter(memory, [])
    visited_fields = {Point(0, 0): Field(Point(0, 0), 0, 0)}

    pos = Point(0, 0)
    dir = Point(0, 1)
    step_counter = 0
    while not instructions.finished:
        new_input = find_field(visited_fields, pos)
        instructions.set_inputs([new_input.color])
        logging.info("Setting input %d on pos %s" % (new_input.color, pos))
        step_counter += 1

        while instructions.process_next_code():
            pass

        new_outputs = instructions.get_outputs()
        output_counter = 0
        while output_counter < len(new_outputs):
            field_to_visit = find_field(visited_fields, pos)
            logging.info("Found field: %s" % field_to_visit)
            field_to_visit.visit(new_outputs[output_counter])
            visited_fields[pos] = field_to_visit
            if new_outputs[output_counter + 1] == 0:
                pos, dir = Point(pos.x + dir.x, pos.y + dir.y), Point(-dir.y, dir.x)
            else:
                pos, dir = Point(pos.x + dir.x, pos.y + dir.y), Point(dir.y, -dir.x)

            output_counter += 2

    print(len(visited_fields))
    print(step_counter)
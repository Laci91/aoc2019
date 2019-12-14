import logging

import file_utils
from intcode_interpreter import IntcodeInterpreter

logging.basicConfig(level=logging.INFO)


class Field:
    def __init__(self, place, color, num_visited):
        self.place = place
        self.color = color
        self.num_visited = num_visited

    def __repr__(self):
        return "Place: (%d, %d); Color: %d; Visited: %d" % (self.place[0], self.place[1], self.color, self.num_visited)

    def visit(self, new_color):
        self.color = new_color
        self.num_visited += 1


def find_field(fields, position):
    return fields[position] if position in fields else Field(pos, 0, 0)


if __name__ == "__main__":
    memory = file_utils.read_comma_delimited_ints("test.txt")
    instructions = IntcodeInterpreter(memory, [0])
    visited_fields = {(0, 0): Field((0, 0), 0, 0)}

    pos = (0, 0)
    dir = (0, 1)
    while not instructions.finished:
        while instructions.process_next_code():
            pass

        new_outputs = instructions.get_outputs()
        logging.info("Output: %s" % new_outputs)
        output_counter = 0
        while output_counter < len(new_outputs):
            field_to_visit = find_field(visited_fields, pos)
            field_to_visit.visit(new_outputs[output_counter])
            visited_fields[pos] = field_to_visit
            if new_outputs[output_counter + 1] == 0:
                pos, dir = (pos[0] + dir[0], pos[1] + dir[1]), (-dir[1], dir[0])
            else:
                pos, dir = (pos[0] + dir[0], pos[1] + dir[1]), (dir[1], -dir[0])

            output_counter += 2

        new_input = find_field(visited_fields, pos)
        logging.info("Provided input: %s" % new_input)
        instructions.set_inputs([new_input.color])

    print(len(visited_fields))

import itertools

import file_utils
from intcode_interpreter import IntcodeInterpreter

if __name__ == "__main__":
    operations = file_utils.read_comma_delimited_ints("input07.txt")
    phase_settings = list(itertools.permutations([0, 1, 2, 3, 4]))
    max_output = -1
    for phase_setting in phase_settings:
        last_output = 0
        for phase in phase_setting:
            inputs = [phase, last_output]
            computer = IntcodeInterpreter(list(operations), inputs)
            while computer.process_next_code():
                pass
            last_output = computer.get_outputs()[0]

        if last_output > max_output:
            max_output = last_output

    print(max_output)

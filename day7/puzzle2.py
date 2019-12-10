import itertools
import logging

import file_utils
from intcode_interpreter import IntcodeInterpreter

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    operations = file_utils.read_comma_delimited_ints("input07.txt")
    phase_settings = list(itertools.permutations([5, 6, 7, 8, 9]))
    max_output = -1
    last_output = 0

    for phase_setting in phase_settings:

        # Initialize
        computers = []
        for i in range(0, len(phase_setting)):
            inputs = [phase_setting[i], 0]
            print ("Phase setting %d is %d" % (i, phase_setting[i]))
            computers.append(IntcodeInterpreter(list(operations), inputs))

        # Start feedback loop
        amplifier = 0
        starting_round = True
        while not computers[4].finished:
            logging.info("Activate computer nr %d" % amplifier)
            logging.info("Instruction pointer is at %d" % computers[amplifier].instruction_pointer)
            logging.info(computers[amplifier].get_memory())
            while computers[amplifier].process_next_code():
                pass
            last_output = computers[amplifier].get_outputs()[-1]
            logging.info("Leaving amplifier %d with new output %d" % (amplifier, last_output))
            amplifier = (amplifier + 1) % 5
            next_inputs = [phase_setting[amplifier], last_output] if starting_round else [last_output]
            computers[amplifier].set_inputs(next_inputs)

            if amplifier == 4:
                starting_round = False

        if last_output > max_output:
            max_output = last_output

    print(max_output)

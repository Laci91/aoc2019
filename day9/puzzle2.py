import logging

import file_utils
from intcode_interpreter import IntcodeInterpreter

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    operations = file_utils.read_comma_delimited_ints("input09.txt")
    interpreter = IntcodeInterpreter(operations, [2])
    while interpreter.process_next_code():
        pass
    print(interpreter.get_outputs())

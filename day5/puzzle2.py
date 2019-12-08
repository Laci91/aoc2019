import file_utils
from intcode_interpreter import IntcodeInterpreter

if __name__ == "__main__":
    operations = file_utils.read_comma_delimited_ints("input05.txt")
    interpreter = IntcodeInterpreter(operations, [5])
    while interpreter.process_next_code():
        pass

    print(interpreter.get_outputs())

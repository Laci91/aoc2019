import file_utils
import intcode_interpreter


if __name__ == "__main__":
    operations = file_utils.read_comma_delimited_ints("input02a.txt")
    operations[1] = 12
    operations[2] = 2
    interpreter = intcode_interpreter.IntcodeInterpreter(operations, [])
    while interpreter.process_next_code():
        pass

    final_operations = interpreter.get_memory()
    print(final_operations[1] * 100 + final_operations[2])

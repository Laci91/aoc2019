import file_utils
import intcode_interpreter


if __name__ == "__main__":
    instructions = file_utils.read_comma_delimited_ints("input13.txt")
    computer = intcode_interpreter.IntcodeInterpreter(instructions, [])

    while computer.process_next_code():
        pass

    outputs = computer.get_outputs()
    print(len([outputs[i:i+3] for i in range(0, len(outputs), 3) if outputs[i+2] == 2]))

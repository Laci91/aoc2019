from intcode_interpreter import IntcodeInterpreter


if __name__ == "__main__":
    base_computer = IntcodeInterpreter.from_file("input19.txt")
    inputs = []
    for x in range(0, 50):
        for y in range(0, 50):
            inputs += [[x, y]]

    beam_count = 0
    for i in inputs:
        computer = IntcodeInterpreter.from_computer(base_computer)
        computer.set_inputs(i)
        while computer.process_next_code():
            pass

        output = computer.get_outputs()[0]
        if output == 1:
            beam_count += 1

    print(beam_count)

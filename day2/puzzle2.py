import file_utils
import intcode_interpreter

MAGIC_NUMBER = 19690720


if __name__ == "__main__":
    operations = file_utils.read_comma_delimited_ints("input02a.txt")
    solution = None
    for noun in range(0, 99):
        for verb in range(0, 99):
            clean_memory = list(operations)
            clean_memory[1] = noun
            clean_memory[2] = verb
            interpreter = intcode_interpreter.IntcodeInterpreter(clean_memory, [])
            while interpreter.process_next_code():
                pass

            print("Noun: %d, Verb: %d = %d" % (noun, verb, clean_memory[0]))
            if clean_memory[0] == MAGIC_NUMBER:
                solution = (noun, verb)
                break

        if solution is not None:
            break

    print(100 * solution[0] + solution[1])

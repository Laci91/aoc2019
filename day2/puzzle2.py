import day2.puzzle1
import util

MAGIC_NUMBER = 19690720


if __name__ == "__main__":
    operations = util.read_comma_delimited_ints("input02a.txt")
    solution = None
    for noun in range(0, 99):
        for verb in range(0, 99):
            result = day2.puzzle1.calculate_int_code(operations, noun, verb)
            print("Noun: %d, Verb: %d = %d" % (noun, verb, result))
            if result == MAGIC_NUMBER:
                solution = (noun, verb)
                break

        if solution is not None:
            break

    print(100 * solution[0] + solution[1])

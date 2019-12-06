import util


def execute_op_code(code_position, code_table):
    op_code = code_table[code_position]
    util.check_position_in_list(code_position + 3, code_table)
    operand1_position = code_table[code_position + 1]
    operand1 = code_table[operand1_position]
    operand2_position = code_table[code_position + 2]
    operand2 = code_table[operand2_position]
    result_position = code_table[code_position + 3]

    if op_code == 1:
        code_table[result_position] = operand1 + operand2
    elif op_code == 2:
        code_table[result_position] = operand1 * operand2
    else:
        raise Exception("Invalid op_code detected at position %s - op_code value is %s" % (code_position, op_code))


def calculate_int_code(ops, noun, verb):
    op_code_position = 0
    memory = list(ops)
    memory[1] = noun
    memory[2] = verb
    while True:
        util.check_position_in_list(op_code_position, memory)
        op_code = memory[op_code_position]
        if op_code == 99:
            break

        execute_op_code(op_code_position, memory)
        op_code_position += 4

    return memory[0]


if __name__ == "__main__":
    operations = util.read_comma_delimited_ints("input02a.txt")
    result = calculate_int_code(operations, 12, 2)
    print(result)

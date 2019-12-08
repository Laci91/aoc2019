from enum import Enum


class ParameterMode(Enum):
    POSITION = 0,
    VALUE = 1


class IntcodeInterpreter:
    def __init__(self, memory, inputs):
        self.instruction_pointer = 0
        self.input_pointer = 0
        self.memory = memory
        self.inputs = inputs
        self.outputs = []

    def get_memory(self):
        return self.memory

    def process_next_code(self):
        op_code_string = "{:05d}".format(self.memory[self.instruction_pointer])
        self.instruction_pointer += 1
        parameter_modes = [int(m) for m in op_code_string[:3]]
        print("Program for op code %s comes up next" % op_code_string)
        op_code = int(op_code_string[-2:])
        if op_code not in [1, 2, 3, 4, 5, 6, 7, 8, 99]:
            raise Exception("Invalid op_code detected: %s" % op_code)

        if op_code == 1:
            self.execute_addition(parameter_modes)
        elif op_code == 2:
            self.execute_multiplication(parameter_modes)
        elif op_code == 3:
            self.read_input()
        elif op_code == 4:
            self.collect_output(parameter_modes)
        elif op_code == 5:
            self.jump_instruction_pointer(True, parameter_modes)
        elif op_code == 6:
            self.jump_instruction_pointer(False, parameter_modes)
        elif op_code == 7:
            self.evaluate_expression(lambda op1, op2: op1 < op2, parameter_modes)
        elif op_code == 8:
            self.evaluate_expression(lambda op1, op2: op1 == op2, parameter_modes)
        elif op_code == 99:
            return False

        return True

    def get_parameter_value(self, parameter_mode):
        place = self.instruction_pointer if parameter_mode == 1 else self.memory[self.instruction_pointer]
        value = self.memory[place]
        print("Read value %s from place %s" % (value, place))
        self.instruction_pointer += 1
        return value

    def set_parameter_value(self, value):
        self.memory[self.memory[self.instruction_pointer]] = value
        print("Set value %s in place %s" % (value, self.memory[self.instruction_pointer]))
        self.instruction_pointer += 1

    def execute_addition(self, parameter_modes):
        print("Running addition")
        param1 = self.get_parameter_value(parameter_modes[2])
        param2 = self.get_parameter_value(parameter_modes[1])
        self.set_parameter_value(param1 + param2)

    def execute_multiplication(self, parameter_modes):
        print("Running multiplication")
        param1 = self.get_parameter_value(parameter_modes[2])
        param2 = self.get_parameter_value(parameter_modes[1])
        self.set_parameter_value(param1 * param2)

    def read_input(self):
        print("Running input expression")
        param1 = self.inputs[self.input_pointer]
        self.input_pointer += 1
        self.set_parameter_value(param1)

    def collect_output(self, parameter_modes):
        param1 = self.get_parameter_value(parameter_modes[2])
        print("Persisting output %d" % param1)
        self.outputs.append(param1)

    def jump_instruction_pointer(self, check_value, parameter_modes):
        param1 = self.get_parameter_value(parameter_modes[2])
        param2 = self.get_parameter_value(parameter_modes[1])
        print("Jump instruction pointer if true: %s == %s" % (param1 != 0, check_value))
        if (param1 != 0) == check_value:
            self.instruction_pointer = param2

    def evaluate_expression(self, expression, parameter_modes):
        param1 = self.get_parameter_value(parameter_modes[2])
        param2 = self.get_parameter_value(parameter_modes[1])
        if expression(param1, param2):
            self.set_parameter_value(1)
        else:
            self.set_parameter_value(0)

    def get_inputs(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs

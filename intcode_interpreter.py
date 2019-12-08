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
        op_code = int(op_code_string[-2:])
        if op_code not in [1, 2, 3, 4, 99]:
            raise Exception("Invalid op_code detected: %s" % op_code)

        if op_code == 1:
            self.execute_addition(parameter_modes)
            return True
        elif op_code == 2:
            self.execute_multiplication(parameter_modes)
            return True
        elif op_code == 3:
            self.read_input()
            return True
        elif op_code == 4:
            self.collect_output(parameter_modes)
            return True
        elif op_code == 99:
            return False

    def get_parameter_value(self, parameter_mode):
        place = self.instruction_pointer if parameter_mode == 1 else self.memory[self.instruction_pointer]
        value = self.memory[place]
        self.instruction_pointer += 1
        return value

    def set_parameter_value(self, value):
        self.memory[self.memory[self.instruction_pointer]] = value
        self.instruction_pointer += 1

    def execute_addition(self, parameter_modes):
        param1 = self.get_parameter_value(parameter_modes[2])
        param2 = self.get_parameter_value(parameter_modes[1])
        self.set_parameter_value(param1 + param2)

    def execute_multiplication(self, parameter_modes):
        param1 = self.get_parameter_value(parameter_modes[2])
        param2 = self.get_parameter_value(parameter_modes[1])
        self.set_parameter_value(param1 * param2)

    def read_input(self):
        param1 = self.inputs[self.input_pointer]
        self.input_pointer += 1
        self.set_parameter_value(param1)

    def collect_output(self, parameter_modes):
        param1 = self.get_parameter_value(parameter_modes[2])
        self.outputs.append(param1)

    def get_inputs(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs

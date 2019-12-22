import copy
import itertools
import logging
from enum import Enum


class ParameterMode(Enum):
    POSITION = 0,
    VALUE = 1


class IntcodeInterpreter:
    def __init__(self, memory, inputs):
        self.instruction_pointer = 0
        self.input_pointer = 0
        self.relative_base = 0
        self.memory = memory
        self.inputs = inputs
        self.waiting_for_input = False
        self.finished = False
        self.outputs = []

    @staticmethod
    def from_computer(computer):
        new_computer = IntcodeInterpreter(copy.deepcopy(computer.memory), [])
        new_computer.instruction_pointer = computer.instruction_pointer
        new_computer.relative_base = computer.relative_base
        new_computer.inputs = []
        new_computer.waiting_for_input = False
        return new_computer

    def get_memory(self):
        return self.memory

    def process_next_code(self):
        logging.debug("Instruction pointer is at %s" % self.instruction_pointer)
        op_code_string = "{:05d}".format(self.memory[self.instruction_pointer])
        self.instruction_pointer += 1
        parameter_modes = [int(m) for m in op_code_string[:3]]
        logging.debug("Program for op code %s comes up next" % op_code_string)
        op_code = int(op_code_string[-2:])
        if op_code not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]:
            raise Exception("Invalid op_code detected: %s" % op_code)

        if op_code == 1:
            self.execute_addition(parameter_modes)
        elif op_code == 2:
            self.execute_multiplication(parameter_modes)
        elif op_code == 3:
            self.read_input(parameter_modes)
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
        elif op_code == 9:
            self.adjust_relative_base(parameter_modes)
        elif op_code == 99:
            self.finished = True
            return False

        if self.waiting_for_input:
            logging.debug("Suspending program until input arrives")
            self.instruction_pointer -= 1
            return False

        return True

    def get_parameter_value(self, parameter_mode):
        place = self.resolve_parameter_place(parameter_mode)
        if place >= len(self.memory):
            self.resize_memory(place + 1)
        value = self.memory[place]
        logging.debug("Read value %s from place %s" % (value, place))
        self.instruction_pointer += 1
        return value

    def resolve_parameter_place(self, parameter_mode):
        if parameter_mode == 0:
            return self.memory[self.instruction_pointer]
        elif parameter_mode == 1:
            return self.instruction_pointer
        elif parameter_mode == 2:
            return self.memory[self.instruction_pointer] + self.relative_base

        raise Exception("Parameter mode %d not recognized" % parameter_mode)

    def set_parameter_value(self, value, parameter_mode):
        if parameter_mode == 2:
            place = self.memory[self.instruction_pointer] + self.relative_base
        else:
            place = self.memory[self.instruction_pointer]

        if place >= len(self.memory):
            self.resize_memory(place + 1)

        self.memory[place] = value
        logging.debug("Set value %s in place %s" % (value, self.memory[self.instruction_pointer]))
        self.instruction_pointer += 1

    def execute_addition(self, parameter_modes):
        logging.debug("Running addition")
        param1 = self.get_parameter_value(parameter_modes[2])
        param2 = self.get_parameter_value(parameter_modes[1])
        self.set_parameter_value(param1 + param2, parameter_modes[0])

    def execute_multiplication(self, parameter_modes):
        logging.debug("Running multiplication")
        param1 = self.get_parameter_value(parameter_modes[2])
        param2 = self.get_parameter_value(parameter_modes[1])
        self.set_parameter_value(param1 * param2, parameter_modes[0])

    def read_input(self, parameter_mode):
        logging.debug("Running input expression")
        if self.input_pointer >= len(self.inputs):
            logging.debug("Waiting for input")
            self.waiting_for_input = True
            return
        else:
            self.waiting_for_input = False
        param1 = self.inputs[self.input_pointer]
        self.input_pointer += 1
        self.set_parameter_value(param1, parameter_mode[2])

    def collect_output(self, parameter_modes):
        param1 = self.get_parameter_value(parameter_modes[2])
        logging.debug("Persisting output %d" % param1)
        self.outputs.append(param1)

    def jump_instruction_pointer(self, check_value, parameter_modes):
        param1 = self.get_parameter_value(parameter_modes[2])
        param2 = self.get_parameter_value(parameter_modes[1])
        logging.debug("Jump instruction pointer if true: %s == %s" % (param1 != 0, check_value))
        if (param1 != 0) == check_value:
            self.instruction_pointer = param2

    def evaluate_expression(self, expression, parameter_modes):
        param1 = self.get_parameter_value(parameter_modes[2])
        param2 = self.get_parameter_value(parameter_modes[1])
        if expression(param1, param2):
            self.set_parameter_value(1, parameter_modes[0])
        else:
            self.set_parameter_value(0, parameter_modes[0])

    def adjust_relative_base(self, parameter_modes):
        param1 = self.get_parameter_value(parameter_modes[2])
        self.relative_base += param1
        logging.debug("Adjusted relative base by %d to %d" % (param1, self.relative_base))

    def get_inputs(self):
        return self.inputs

    def set_inputs(self, inputs):
        self.inputs = inputs
        self.input_pointer = 0

    def get_outputs(self):
        outputs = self.outputs
        self.outputs = []
        return outputs

    def resize_memory(self, new_size):
        new_memory = list(itertools.repeat(0, new_size))
        new_memory[0:len(self.memory)] = self.memory
        self.memory = new_memory

import logging

import file_utils
import intcode_interpreter
from point import Point

logging.basicConfig(level=logging.INFO)


def process_outputs(output):
    ball = None
    paddle = None
    score = None
    output_triplets = [output[i:i + 3] for i in range(0, len(output), 3)]
    for triplet in output_triplets:
        if triplet[0] == -1 and triplet[1] == 0:
            score = triplet[2]
        elif triplet[2] == 4:
            ball = Point(triplet[0], triplet[1])
        elif triplet[2] == 3:
            paddle = Point(triplet[0], triplet[1])

    return paddle, ball, score


if __name__ == "__main__":
    instructions = file_utils.read_comma_delimited_ints("input13.txt")
    instructions[0] = 2
    computer = intcode_interpreter.IntcodeInterpreter(instructions, [])

    paddle_pos = None
    ball_pos = None
    high_score = None

    while not computer.finished:
        while computer.process_next_code():
            pass

        processed_output = process_outputs(computer.get_outputs())
        paddle_pos = processed_output[0] if processed_output[0] is not None else paddle_pos
        ball_pos = processed_output[1] if processed_output[1] is not None else ball_pos
        high_score = processed_output[2] if processed_output[2] is not None else high_score
        print("Ball: %s, Paddle: %s, Score: %s" % (ball_pos, paddle_pos, high_score))
        if paddle_pos.x > ball_pos.x:
            computer.set_inputs([-1])
        elif paddle_pos.x < ball_pos.x:
            computer.set_inputs([1])
        else:
            computer.set_inputs([0])

    print(high_score)

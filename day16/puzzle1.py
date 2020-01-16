from itertools import chain

import file_utils

MULTI_FACTOR = 10000


def run_phase(input_signal, pattern):
    output_signal = []
    for i in range(1, len(input_signal) + 1):
        print("%dth character" % i)
        if MULTI_FACTOR % 4*i == 0:
            factor = MULTI_FACTOR / 4*i
            positive = sum(chain.from_iterable(
                [input_signal[l:l + i * 4][i - 1:i * 2 - 1] for l in range(0, len(input_signal) // MULTI_FACTOR, i * 4)]))
            negative = sum(chain.from_iterable(
                [input_signal[l:l + i * 4][i * 3 - 1:i * 4 - 1] for l in range(0, len(input_signal) // MULTI_FACTOR, i * 4)]))
            output_signal.append(abs(positive - negative)*factor % 10)
        else:
            positive = sum(chain.from_iterable([input_signal[l:l+i*4][i-1:i*2-1] for l in range(0, len(input_signal), i*4)]))
            negative = sum(chain.from_iterable([input_signal[l:l+i*4][i*3-1:i*4-1] for l in range(0, len(input_signal), i*4)]))
            output_signal.append(abs(positive - negative) % 10)

    return output_signal


if __name__ == "__main__":
    signal_string = file_utils.read("input16.txt")
    signal = [int(ch) for ch in signal_string] * MULTI_FACTOR
    next_input = signal
    for i in range(0, 100):
        print("Iteration %d" % i)
        next_input = run_phase(next_input, [0, 1, 0, -1])

    print(next_input[:8])



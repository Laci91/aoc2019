from collections import Counter

import file_utils

if __name__ == "__main__":
    input_data = file_utils.read("input08.txt")
    width = 25
    height = 6
    layer_length = width * height

    layers = [input_data[i:i+layer_length] for i in range(0, len(input_data), layer_length)]
    min_zero_count = layer_length
    output_value = -1

    for layer in layers:
        c = Counter(layer)
        if c['0'] < min_zero_count:
            min_zero_count = c['0']
            output_value = c['1'] * c['2']

    print(output_value)

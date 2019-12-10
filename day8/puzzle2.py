import file_utils


if __name__ == "__main__":
    input_data = file_utils.read("input08.txt")
    width = 25
    height = 6
    layer_length = width * height

    layers = [input_data[i:i+layer_length] for i in range(0, len(input_data), layer_length)]

    solution = []
    transparent_count = layer_length

    # Initialize to transparent (imagine it like the 0th layer)
    for h in range(0, height):
        solution.append([])

        for w in range(0, width):
            solution[h].append(2)

    # Fill picture until all transparent pixels disappear
    for layer in layers:
        for pixel in range(0, len(layer)):
            h = pixel // width
            w = pixel % width
            print("(%d,%d) for pixel %d" % (h, w, pixel))
            if solution[h][w] == 2 and int(layer[pixel]) != 2:
                solution[h][w] = int(layer[pixel])
                transparent_count -= 1

            if transparent_count == 0:
                break

    print("\n".join(["".join(["%" if pixel == 1 else " " for pixel in lst]) for lst in solution]))

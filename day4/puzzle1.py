from collections import Counter


def convert(i, j, k, l, m, n):
    return i * 100000 + j * 10000 + k * 1000 + l * 100 + m * 10 + n


def get_number_of_passwords(low, high):
    low_str = str(low)
    digits = [int(d) for d in low_str]
    counter = 0
    for i in range(digits[0], 10):
        for j in range(i, 10):
            for k in range(j, 10):
                for l in range(k, 10):
                    for m in range(l, 10):
                        for n in range(m, 10):
                            if convert(i, j, k, l, m, n) >= high:
                                return counter
                            freq = Counter([i, j, k, l, m, n])
                            if any([value > 1 for (key, value) in freq.items()]):
                                counter += 1


if __name__ == "__main__":
    range_low_end = 402328
    range_high_end = 864247

    print(get_number_of_passwords(range_low_end, range_high_end))

def read_lines(filename):
    with open(filename, "r") as f:
        return f.readlines()


def read_comma_delimited(filename):
    with open(filename, "r") as f:
        return f.read().split(",")


def read_ints(filename):
    return [int(line) for line in read_lines(filename)]


def read_comma_delimited_ints(filename):
    return [int(line) for line in read_comma_delimited(filename)]
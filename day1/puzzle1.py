import util


def calculate_fuel_req(weight):
    return weight // 3 - 2


if __name__ == "__main__":
    lines = util.read_ints("input01a.txt")
    print(sum([calculate_fuel_req(weight) for weight in lines]))


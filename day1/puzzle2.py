import util


def calculate_fuel_req(weight):
    return weight // 3 - 2


def calculate_full_fuel_req(current_weight, full_fuel_req):
    next_stage = calculate_fuel_req(current_weight)
    if next_stage <= 0:
        return full_fuel_req

    return calculate_full_fuel_req(next_stage, full_fuel_req + next_stage)


if __name__ == "__main__":
    lines = util.read_ints("input01b.txt")
    print(sum([calculate_full_fuel_req(weight, 0) for weight in lines]))


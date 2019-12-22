import itertools

import parse

import file_utils

MOON_NAMES = ["Io", "Europa", "Callisto", "Ganymede"]


class Moon:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0

    def calculate_velocity(self, other_moon):
        self.velocity_x += -1 if other_moon.x < self.x else 1 if other_moon.x > self.x else 0
        self.velocity_y += -1 if other_moon.y < self.y else 1 if other_moon.y > self.y else 0
        self.velocity_z += -1 if other_moon.z < self.z else 1 if other_moon.z > self.z else 0

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.z += self.velocity_z

    def calculate_energy(self):
        sit_energy = abs(self.x) + abs(self.y) + abs(self.z)
        kin_energy = abs(self.velocity_x) + abs(self.velocity_y) + abs(self.velocity_z)
        return sit_energy * kin_energy

    def __repr__(self):
        return "Name: %s, Place: (%d, %d, %d)" % (self.name, self.x, self.y, self.z)


def calculate_velocity(m1, m2):
    return (m1 - m2) / abs(m1 - m2)


if __name__ == "__main__":
    lines = file_utils.read_lines("input12.txt")
    moons = []
    counter = 0
    parser = parse.Parser("<x={}, y={}, z={}>")
    for line in lines:
        coordinates = parser.parse(line)
        moons.append(Moon(MOON_NAMES[counter], int(coordinates[0]), int(coordinates[1]), int(coordinates[2])))
        counter += 1

    for i in range(0, 1000000):
        velocities = [{moon, (0, 0, 0)} for moon in moons]
        combinations = itertools.combinations(moons, 2)
        for combination in combinations:
            combination[0].calculate_velocity(combination[1])
            combination[1].calculate_velocity(combination[0])

        for moon in moons:
            moon.move()

        # print(moons)

    for moon in moons:
        print("Name: %s - Energy: %d" % (moon.name, moon.calculate_energy()))

    print("Total energy: %d" % sum(map(lambda m: m.calculate_energy(), moons)))



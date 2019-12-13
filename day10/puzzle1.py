import logging

import file_utils

logging.basicConfig(level=logging.INFO)


def get_slope(num1, num2):
    n1 = max(abs(num1), abs(num2))
    n2 = min(abs(num1), abs(num2))

    if n1 == 0:
        return 0, 0
    if n2 == 0:
        return num1 / n1, num2 / n1

    while n1 % n2 != 0:
        temp = n2
        n2 = n1 % temp
        n1 = temp

    return num1 / n2, num2 / n2


def find_detectable_asteroids(asteroid_map, x, y):
    detectable_asteroids = set()
    for n in range(0, len(asteroid_map)):
        for m in range(0, len(asteroid_map[i])):
            if asteroid_map[n][m]:
                slope = get_slope(x - n, y - m)
                if slope not in detectable_asteroids:
                    logging.debug("Found visible asteroid %s, %s" % (n, m))
                    detectable_asteroids.add(slope)
                else:
                    logging.debug("Asteroid %s, %s is not visible - slope is %s, %s" % (n, m, slope[0], slope[1]))

    return len(detectable_asteroids)


if __name__ == "__main__":
    lines = file_utils.read_lines("input10.txt")
    asteroids = []
    for i in range(0, len(lines)):
        asteroids.append([])

        for j in range(0, len(lines[i])):
            asteroids[i].append(lines[i][j] == "#")

    max_detectable = -1
    for i in range(0, len(asteroids)):
        for j in range(0, len(asteroids[i])):
            logging.info("Checking %s, %s" % (i, j))
            if asteroids[i][j]:
                num = find_detectable_asteroids(asteroids, i, j) - 1
                logging.info("Found %s visible asteroids" % num)
                if num > max_detectable:
                    print("Found better spot at %s, %s with %s visible asteroids" % (i, j, num))
                    max_detectable = num

    print(max_detectable)
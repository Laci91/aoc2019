import itertools
import logging

import file_utils

logging.basicConfig(level=logging.INFO)


class AsteroidPriority:
    def __init__(self, coordinate, station):
        self.coordinate = coordinate
        x = coordinate[0] - station[0]
        y = coordinate[1] - station[1]
        slope = get_slope(x, y)
        logging.debug("Setting up asteroid: (%s, %s), slope: %s" % (coordinate[0], coordinate[1], slope[0]))
        self.slope = slope[0]
        self.priority = slope[1]
        if x >= 0 and y < 0:
            self.quarter = 1
        elif x > 0 and y >= 0:
            self.quarter = 2
        elif x <= 0 and y > 0:
            self.quarter = 3
        else:
            self.quarter = 4

    def __repr__(self):
        return "X,Y: (%s, %s) - Slope: %f - Priority: %d - Quarter: %d" % (self.coordinate[0], self.coordinate[1], self.slope, self.priority, self.quarter)


def get_slope(num1, num2):
    if num2 == 0:
        return float("infinity"), abs(num1)
    if num1 == 0:
        return 0, abs(num2)

    n1 = max(abs(num1), abs(num2))
    n2 = min(abs(num1), abs(num2))

    while n1 % n2 != 0:
        temp = n2
        n2 = n1 % temp
        n1 = temp

    return num1 / num2, n2


def prioritize_asteroids(asteroid_map, station):
    asteroid_priorities = []
    for n in range(0, len(asteroid_map)):
        for m in range(0, len(asteroid_map[i])):
            if asteroid_map[n][m]:
                asteroid_priorities.append(AsteroidPriority((n, m), station))

    return asteroid_priorities


if __name__ == "__main__":
    lines = file_utils.read_lines("input10.txt")
    asteroids = []
    for i in range(0, len(lines[0])):
        asteroids.append([])

        for j in range(0, len(lines)):
            asteroids[i].append(lines[j][i] == "#")

    priorities = prioritize_asteroids(asteroids, (22, 28))

    active_quarter = 1
    removed_asteroid_count = 0
    last_removed_asteroid = None
    while removed_asteroid_count < 200 and len(priorities) > 0:
        asteroids_in_active_quarter = [asteroid for asteroid in priorities if asteroid.quarter == active_quarter]
        sorted_asteroids_in_active_quarter = sorted(asteroids_in_active_quarter, key=lambda a: a.slope, reverse=True)
        grouped_asteroids = [list(v) for k, v in itertools.groupby(sorted_asteroids_in_active_quarter, lambda a: a.slope)]
        logging.debug("Group for quarter %d: %s" % (active_quarter, grouped_asteroids))
        shot_asteroids = [min(asteroids, key=lambda a: a.priority) for asteroids in grouped_asteroids]
        for asteroid in shot_asteroids:
            logging.debug("Shooting asteroid %s, %s - slope is %f, with priority %d" % (asteroid.coordinate[0], asteroid.coordinate[1], asteroid.slope, asteroid.priority))
            priorities.remove(asteroid)
            removed_asteroid_count += 1
            last_removed_asteroid = asteroid
            if removed_asteroid_count == 200:
                break

        active_quarter = active_quarter % 4 + 1
        logging.debug("Moving to next quarter: %d" % active_quarter)

    print(last_removed_asteroid)
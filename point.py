class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "X: %d, Y: %d" % (self.x, self.y)

    def __hash__(self):
        return self.x * 1000000 + self.y

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y

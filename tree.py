class Node:
    def __init__(self, parent):
        self.parent = parent
        if parent is not None:
            self.parent.add_child(self)
        self.children = []
        self.value = None

    def get_value(self):
        return self.value

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def add_parent(self, parent):
        self.parent = parent
        parent.add_child(self)

    def is_leaf(self):
        return len(self.children) == 0

    def is_root(self):
        return self.parent is None

    def logger(self):
        pass

    def depth_first_walk(self, value_function, propagator_function):
        for child in self.children:
            child.depth_first_walk(value_function, propagator_function)

        if self.is_leaf():
            self.value = value_function(self)
        else:
            self.value = propagator_function(self)

        self.logger()

    def breadth_first_walk(self, value_function, propagator_function):
        if self.is_root():
            self.value = value_function(self)
        else:
            self.value = propagator_function(self)

        for child in self.children:
            child.breadth_first_walk(value_function, propagator_function)


class PlanetOrbitNode(Node):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.name = name

    def logger(self):
        print("Function invoked on %s, value is %d" % (self.name, self.value))

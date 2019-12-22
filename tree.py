class Node:
    def __init__(self, parent):
        self.parent = parent
        if parent is not None:
            self.parent.add_child(self)
        self.children = []
        self.value = None

    def __init__(self, parameters):
        self.__init__(parameters[0])

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


def build_tree(items, node_factory):
    nodes = {}
    parent_relationships = {}
    root = None
    for item in items:
        parent_item = item[0]
        child_item = item[1]
        nodes[child_item] = node_factory([None, child_item])
        if parent_item in parent_relationships:
            parent_relationships[parent_item].append(child_item)
        else:
            parent_relationships[parent_item] = [child_item]

    for parent in parent_relationships:
        if parent not in nodes:
            root = node_factory([None, parent])
            nodes[parent] = root

        for child in parent_relationships[parent]:
            nodes[child].add_parent(nodes[parent])

    if root is None:
        raise Exception("Root element not found in tree")
    return root


class PlanetOrbitNode(Node):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.name = name

    def __init__(self, parameters):
        self.__init__(parameters[0], parameters[1])

    def logger(self):
        print("Function invoked on %s, value is %d" % (self.name, self.value))

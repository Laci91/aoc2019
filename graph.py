class Node:
    def __init__(self, name):
        self.connections = []
        self.value = None
        self.name = name

    def get_value(self):
        return self.value

    def add_connection(self, node):
        self.connections.append(node)
        node.connections.append(self)

    def depth_first_walk(self, function):
        self.depth_first_walk_internal(self, function)

    def depth_first_walk_internal(self, messenger_node, function):
        if self.value is None:
            for child in self.connections:
                child.depth_first_walk_internal(self, function)

            self.value = function(messenger_node)

    def breadth_first_walk(self, function):
        self.breadth_first_walk_internal(self, function, True)

    def breadth_first_walk_internal(self, messenger_node, function, starting_point):
        if starting_point or self.value is None:
            self.value = function(messenger_node)
            print("Set value %d for node %s" % (self.value, self.name))

            for child in self.connections:
                child.breadth_first_walk_internal(self, function, False)

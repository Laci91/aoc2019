import file_utils
from graph import Node
from point import Point


class RecursiveValue:
    def __init__(self, value, level):
        self.name = value
        self.level = level


def handle_entry_point(labyrinth, x, y):
    print("Found entry point %s at (%d, %d)" % (labyrinth[x][y], x, y))


def is_entry_point(labyrinth, x, y):
    if labyrinth[x][y].isalpha():
        if 0 < x < len(labyrinth) - 1 and y < len(labyrinth[x + 1]) and labyrinth[x + 1][y].isalpha() and \
                labyrinth[x - 1][y] == ".":
            return labyrinth[x][y] + labyrinth[x + 1][y]
        
        if 0 < x < len(labyrinth) - 1 and y < len(labyrinth[x + 1]) and labyrinth[x - 1][y].isalpha() and \
                labyrinth[x + 1][y] == ".":
            if labyrinth[x][y] == "Z":
                print(".")
            return labyrinth[x - 1][y] + labyrinth[x][y]
        
        if 0 < y < len(labyrinth[x]) - 1 and labyrinth[x][y - 1].isalpha() and labyrinth[x][y + 1] == ".":
            return labyrinth[x][y - 1] + labyrinth[x][y]
        
        if 0 < y < len(labyrinth[x]) - 1 and labyrinth[x][y + 1].isalpha() and labyrinth[x][y - 1] == ".":
            return labyrinth[x][y] + labyrinth[x][y + 1]
    
    return None


if __name__ == "__main__":
    labyrinth = file_utils.read_lines("input20.txt")
    final_map = {}
    entry_points = {}
    for i in range(0, len(labyrinth)):
        for j in range(0, len(labyrinth[i])):
            node = None
            if labyrinth[i][j] == ".":
                node = Node("")
                final_map[Point(i, j)] = node
            
            entry_point = is_entry_point(labyrinth, i, j)
            if entry_point and entry_point not in entry_points:
                node = Node(entry_point)
                final_map[Point(i, j)] = node
                entry_points[node.name] = node
            elif entry_point:
                node = entry_points[entry_point]
                final_map[Point(i, j)] = node
            
            if node:
                print("%s = (%s, %s)" % (entry_point, i, j))
                if Point(i - 1, j) in final_map:
                    print("(%s, %s) => (%s, %s)" % (i, j, i - 1, j))
                    final_map[Point(i - 1, j)].add_connection(node)
                if Point(i + 1, j) in final_map:
                    final_map[Point(i + 1, j)].add_connection(node)
                    print("(%s, %s) => (%s, %s)" % (i, j, i + 1, j))
                if Point(i, j - 1) in final_map:
                    final_map[Point(i, j - 1)].add_connection(node)
                    print("(%s, %s) => (%s, %s)" % (i, j, i, j - 1))
                if Point(i, j + 1) in final_map:
                    final_map[Point(i, j + 1)].add_connection(node)
                    print("(%s, %s) => (%s, %s)" % (i, j, i, j + 1))
    
    entry_points["AA"].value = 0
    next_nodes = [entry_points["AA"]]
    modified_connections = []
    while len(next_nodes) > 0:
        current_node = next_nodes.pop(0)
        child_node_value = current_node.value + 1 if current_node.name == "" else current_node.value
        modified_connections = []
        print("New current: %s" % current_node)
        
        for node in current_node.connections:
            if node.value is None or node.value > child_node_value:
                node.value = child_node_value
                modified_connections.append(node)
        
        next_nodes.extend(modified_connections)
        # print("Next: %s" % next_nodes)
    
    print(entry_points["ZZ"].value - 1)

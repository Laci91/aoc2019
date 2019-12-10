import file_utils
from tree import PlanetOrbitNode


def build_tree(orbits):
    nodes = {}
    parent_relationships = {}
    root = None
    for orbit_pair in orbits:
        parent_planet = orbit_pair[0]
        child_planet = orbit_pair[1]
        nodes[child_planet] = PlanetOrbitNode(None, child_planet)
        if parent_planet in parent_relationships:
            parent_relationships[parent_planet].append(child_planet)
        else:
            parent_relationships[parent_planet] = [child_planet]

    for parent in parent_relationships:
        if parent not in nodes:
            root = PlanetOrbitNode(None, parent)
            nodes[parent] = root

        for child in parent_relationships[parent]:
            nodes[child].add_parent(nodes[parent])

    if root is None:
        raise Exception("Root element not found in tree")
    return root


if __name__ == "__main__":
    orbit_input = file_utils.read_parenthesis_delimited("input06.txt")
    parent_node = build_tree(orbit_input)
    # Assign levels (number of direct and indirect orbits) to each node
    parent_node.breadth_first_walk(lambda nd: 0, lambda nd: nd.parent.value + 1)
    # Roll up levels from leafs up to the root
    parent_node.depth_first_walk(lambda nd: nd.value, lambda nd: sum(map(lambda n: n.value, nd.children)) + nd.value)
    print(parent_node.value)

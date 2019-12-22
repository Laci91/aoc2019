import file_utils
import tree


if __name__ == "__main__":
    orbit_input = file_utils.read_parenthesis_delimited("input06.txt")
    parent_node = tree.build_tree(orbit_input, lambda children: tree.PlanetOrbitNode(None, children))
    # Assign levels (number of direct and indirect orbits) to each node
    parent_node.breadth_first_walk(lambda nd: 0, lambda nd: nd.parent.value + 1)
    # Roll up levels from leafs up to the root
    parent_node.depth_first_walk(lambda nd: nd.value, lambda nd: sum(map(lambda n: n.value, nd.children)) + nd.value)
    print(parent_node.value)

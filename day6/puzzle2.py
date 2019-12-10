import file_utils
from graph import Node


def build_graph(orbits):
    nodes = {}
    for orbit_pair in orbits:
        planet1 = orbit_pair[0]
        planet2 = orbit_pair[1]
        if planet1 not in nodes:
            nodes[planet1] = Node(planet1)
        if planet2 not in nodes:
            nodes[planet2] = Node(planet2)

        nodes[planet1].add_connection(nodes[planet2])

    return nodes


if __name__ == "__main__":
    orbit_input = file_utils.read_parenthesis_delimited("input06.txt")
    node_mappings = build_graph(orbit_input)
    node_mappings["YOU"].value = 0
    node_mappings["YOU"].breadth_first_walk(lambda nd: nd.value + 1)
    print(node_mappings["SAN"].value - 3)

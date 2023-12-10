from itertools import chain


class Node:
    def __init__(self, x, y, contents):
        self.x = x
        self.y = y
        self.contents = contents

    def loc_str(self):
        return '{},{}'.format(self.x, self.y)


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)

    def start_node(self):
        for y, line in enumerate(self.lines):
            for x, contents in enumerate(line):
                if contents == 'S':
                    return Node(x, y, contents)

    def connected_nodes(self):
        start_node = self.start_node()
        connected_by_location = {start_node.loc_str(): start_node}
        nodes = [start_node]
        while len(nodes) > 0:
            nodes = list(filter(lambda n: n.loc_str() not in connected_by_location,
                                chain.from_iterable(map(self.next_nodes_of, nodes))))
            for node in nodes:
                connected_by_location[node.loc_str()] = node
        return connected_by_location.values()

    def nodes_in_path(self):
        return [self.start_node()]

    def next_nodes_of(self, node):
        return filter(lambda n: n is not None, [
            self.left_connection_of(node),
            self.right_connection_of(node)
        ])

    def left_connection_of(self, node):
        if node.x == 0:
            return None
        if node.contents not in ('-', 'J', '7', 'S'):
            return None
        left = self.node_at(node.x - 1, node.y)
        if left.contents not in ('-', 'F', 'L'):
            return None
        return left

    def right_connection_of(self, node):
        if node.x == self.width - 1:
            return None
        if node.contents not in ('-', 'F', 'L', 'S'):
            return None
        right = self.node_at(node.x + 1, node.y)
        if right.contents not in ('-', 'J', '7'):
            return None
        return right

    def node_at(self, x, y):
        return Node(x, y, self.lines[y][x])


def read_grid_from_file(input_file):
    with open(input_file, 'r') as file:
        raw_lines = file.readlines()
    return Grid(list(map(lambda ln: ln.strip(), raw_lines)))

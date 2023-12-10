class Node:
    def __init__(self, x, y, contents):
        self.x = x
        self.y = y
        self.contents = contents

    def loc_str(self):
        return '{},{}'.format(self.x, self.y)


def contents_connect(prev_node, next_node, prev_contents, next_contents):
    if prev_node.contents != 'S' and prev_node.contents not in prev_contents:
        return False
    if next_node.contents not in next_contents:
        return False
    return True


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
        connected_by_location = {}
        nodes = [start_node]
        node = start_node
        while True:
            nodes.append(node)
            connected_by_location[node.loc_str()] = node
            next_nodes = list(filter(lambda n: n.loc_str() not in connected_by_location,
                                     self.next_nodes_of(node)))
            if len(next_nodes) == 0:
                return nodes
            node = next_nodes[0]

    def furthest_position_on_path(self):
        return int(len(self.connected_nodes()) / 2)

    def next_nodes_of(self, node):
        return filter(lambda n: n is not None, [
            self.left_connection_of(node),
            self.right_connection_of(node),
            self.top_connection_of(node),
            self.bottom_connection_of(node)
        ])

    def left_connection_of(self, node):
        if node.x == 0:
            return None
        left = self.node_at(node.x - 1, node.y)
        if contents_connect(node, left,
                            ('-', 'J', '7'),
                            ('-', 'F', 'L')):
            return left
        else:
            return None

    def right_connection_of(self, node):
        if node.x == self.width - 1:
            return None
        right = self.node_at(node.x + 1, node.y)
        if contents_connect(node, right,
                            ('-', 'F', 'L'),
                            ('-', 'J', '7')):
            return right
        else:
            return None

    def top_connection_of(self, node):
        if node.y == 0:
            return None
        top = self.node_at(node.x, node.y - 1)
        if contents_connect(node, top,
                            ('|', 'J', 'L'),
                            ('|', 'F', '7')):
            return top
        else:
            return None

    def bottom_connection_of(self, node):
        if node.y == self.height - 1:
            return None
        bottom = self.node_at(node.x, node.y + 1)
        if contents_connect(node, bottom,
                            ('|', 'F', '7'),
                            ('|', 'J', 'L')):
            return bottom
        else:
            return None

    def node_at(self, x, y):
        return Node(x, y, self.lines[y][x])


def read_grid_from_file(input_file):
    with open(input_file, 'r') as file:
        raw_lines = file.readlines()
    return Grid(list(map(lambda ln: ln.strip(), raw_lines)))

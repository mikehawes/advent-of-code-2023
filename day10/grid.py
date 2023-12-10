from itertools import chain


def loc_str(x, y):
    return '{},{}'.format(x, y)


class Node:
    def __init__(self, x, y, contents):
        self.x = x
        self.y = y
        self.contents = contents

    def loc_str(self):
        return loc_str(self.x, self.y)


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

    def connected_pipes_of(self, pipe):
        return filter(lambda n: n is not None, (
            self.left_pipe_connection(pipe),
            self.right_pipe_connection(pipe),
            self.top_pipe_connection(pipe),
            self.bottom_pipe_connection(pipe)
        ))

    def adjacent_nodes_of(self, node):
        return filter(lambda n: n is not None, (
            self.left_of(node),
            self.right_of(node),
            self.above(node),
            self.below(node)
        ))

    def left_pipe_connection(self, node):
        found = self.left_of(node)
        if found and contents_connect(node, found,
                                      ('-', 'J', '7'),
                                      ('-', 'F', 'L')):
            return found
        else:
            return None

    def left_of(self, node):
        if node.x == 0:
            return None
        return self.node_at(node.x - 1, node.y)

    def right_pipe_connection(self, node):
        found = self.right_of(node)
        if found and contents_connect(node, found,
                                      ('-', 'F', 'L'),
                                      ('-', 'J', '7')):
            return found
        else:
            return None

    def right_of(self, node):
        if node.x == self.width - 1:
            return None
        return self.node_at(node.x + 1, node.y)

    def top_pipe_connection(self, node):
        found = self.above(node)
        if found and contents_connect(node, found,
                                      ('|', 'J', 'L'),
                                      ('|', 'F', '7')):
            return found
        else:
            return None

    def above(self, node):
        if node.y == 0:
            return None
        return self.node_at(node.x, node.y - 1)

    def bottom_pipe_connection(self, node):
        found = self.below(node)
        if found and contents_connect(node, found,
                                      ('|', 'F', '7'),
                                      ('|', 'J', 'L')):
            return found
        else:
            return None

    def below(self, node):
        if node.y == self.height - 1:
            return None
        return self.node_at(node.x, node.y + 1)

    def outer_nodes(self):
        return chain.from_iterable((
            map(lambda n: self.node_at(n, 0), range(0, self.width)),  # top side
            map(lambda n: self.node_at(0, n), range(1, self.height - 1)),  # left side
            map(lambda n: self.node_at(self.width - 1, n), range(1, self.height - 1)),  # right side
            map(lambda n: self.node_at(n, self.height - 1), range(0, self.width))  # bottom side
        ))

    def node_at(self, x, y):
        return Node(x, y, self.lines[y][x])

    def num_nodes(self):
        return self.height * self.width


class Path:
    def __init__(self, grid, start_node):
        self.grid = grid
        self.start_node = start_node
        nodes_by_loc_str = {}
        nodes = []
        node = start_node
        while True:
            nodes.append(node)
            nodes_by_loc_str[node.loc_str()] = node
            next_nodes = list(filter(lambda n: n.loc_str() not in nodes_by_loc_str,
                                     grid.connected_pipes_of(node)))
            if len(next_nodes) == 0:
                break
            node = next_nodes[0]
        self.nodes = nodes
        self.nodes_by_loc_str = nodes_by_loc_str

    def furthest_position(self):
        return int(len(self.nodes) / 2)

    def count_enclosed_tiles(self):
        return self.grid.num_nodes() - len(self.nodes) - len(self.outside_tiles_by_loc_str().values())

    def outside_tiles_by_loc_str(self):
        outside_by_loc_str = {}
        for outer_node in self.grid.outer_nodes():
            self.add_connected_outside_tiles(outer_node, outside_by_loc_str)
        return outside_by_loc_str

    def add_connected_outside_tiles(self, outer_node, outside_by_loc_str):
        loc_str = outer_node.loc_str()
        if loc_str in outside_by_loc_str or loc_str in self.nodes_by_loc_str:
            return
        outside_by_loc_str[loc_str] = outer_node
        for adjacent in self.grid.adjacent_nodes_of(outer_node):
            self.add_connected_outside_tiles(adjacent, outside_by_loc_str)

    def is_uncounted_outside(self, node, outside_by_loc_str):
        loc_str = node.loc_str()
        return loc_str not in outside_by_loc_str and loc_str not in self.nodes_by_loc_str


def read_grid_from_file(input_file):
    with open(input_file, 'r') as file:
        raw_lines = file.readlines()
    return Grid(list(map(lambda ln: ln.strip(), raw_lines)))

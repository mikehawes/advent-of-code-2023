class Node:
    def __init__(self, x, y, contents):
        self.x = x
        self.y = y
        self.contents = contents


class Grid:
    def __init__(self, lines):
        self.lines = lines

    def start_node(self):
        for y, line in enumerate(self.lines):
            for x, contents in enumerate(line):
                if contents == 'S':
                    return Node(x, y, contents)

    def nodes_in_path(self):
        return []


def read_grid_from_file(input_file):
    with open(input_file, 'r') as file:
        raw_lines = file.readlines()
    return Grid(list(map(lambda ln: ln.strip(), raw_lines)))

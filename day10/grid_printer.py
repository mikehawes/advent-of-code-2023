import io


def print_grid(grid):
    output = io.StringIO()
    for line in grid.lines:
        print(line, file=output)
    return output.getvalue()


def print_node(node):
    return '{} at {},{}'.format(node.contents, node.x, node.y)


def node_in_path_at(nodes, x, y):
    for node in nodes:
        if node.x == x and node.y == y:
            return node
    return None


def print_path_in_grid(nodes, grid):
    output = io.StringIO()
    for y, line in enumerate(grid.lines):
        for x, contents in enumerate(line):
            path_node = node_in_path_at(nodes, x, y)
            if path_node:
                output.write(path_node.contents)
            else:
                output.write('.')
        print('', file=output)
    return output.getvalue()

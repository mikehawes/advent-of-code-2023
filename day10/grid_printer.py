import io

from day10.grid import Path


def listed_node_at(nodes, x, y):
    for node in nodes:
        if node.x == x and node.y == y:
            return node
    return None


def print_nodes_in_grid(nodes, grid, output=None):
    if not output:
        output = io.StringIO()
    for y, line in enumerate(grid.lines):
        for x, contents in enumerate(line):
            path_node = listed_node_at(nodes, x, y)
            if path_node:
                output.write(path_node.contents)
            else:
                output.write('.')
        print('', file=output)
    return output.getvalue()


def print_answers(grid):
    path = Path(grid, grid.start_node())
    output = io.StringIO()
    print('Furthest position on path:', path.furthest_position(), file=output)
    print('Enclosed tiles:', path.count_enclosed_tiles(), file=output)
    print(file=output)
    print_nodes_in_grid(path.nodes, grid, output)
    return output.getvalue()

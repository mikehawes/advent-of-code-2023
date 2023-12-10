import io

from day10.grid import Path, to_loc_str


def listed_node_at(nodes, x, y):
    for node in nodes:
        if node.x == x and node.y == y:
            return node
    return None


def print_outside(grid, path, output):
    outside_by_loc_str = path.outside_nodes_by_loc_str()
    for y, line in enumerate(grid.lines):
        for x, contents in enumerate(line):
            path_node = listed_node_at(path.nodes, x, y)
            if path_node:
                output.write(path_node.contents)
            elif to_loc_str(x, y) in outside_by_loc_str:
                output.write('O')
            else:
                output.write('*')
        print('', file=output)
    return output.getvalue()


def print_answers(grid):
    path = Path(grid, grid.start_node())
    output = io.StringIO()
    print('Furthest position on path:', path.furthest_position(), file=output)
    print('Enclosed tiles:', path.count_enclosed_tiles(), file=output)
    print(file=output)
    print_outside(grid, path, output)
    return output.getvalue()

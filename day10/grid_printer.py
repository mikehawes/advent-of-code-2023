import io


def print_grid(grid):
    output = io.StringIO()
    for line in grid.lines:
        print(line, file=output)
    return output.getvalue()


def print_node(node):
    return '{} at {},{}'.format(node.contents, node.x, node.y)

def print_trails_map(trails):
    return '\n'.join(map(lambda line: ''.join(line), trails.tiles))

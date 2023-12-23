import io

from day23.map import Location


def print_trails_map(trails):
    out = io.StringIO()
    for y, line in enumerate(trails.tiles):
        new_line = []
        for x, tile in enumerate(line):
            location = Location(x, y)
            if tile == '.' and location in trails.trail_by_loc:
                trail = trails.trail_by_loc[location]
                new_line.append(label_for_index(trail.number))
            elif tile == '#':
                new_line.append(' ')
            else:
                new_line.append(tile)
        print(''.join(new_line).rstrip(), file=out)
    return out.getvalue()


def label_for_index(index):
    letter_index = index % 26
    return chr(ord('A') + letter_index)

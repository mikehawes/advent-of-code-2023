import io

from day23.map import Location, TrailsMap


def print_trails_map(trails: TrailsMap):
    out = io.StringIO()
    for y in range(0, trails.height):
        new_line = []
        for x in range(0, trails.width):
            location = Location(x, y)
            new_line.append(print_tile(location, trails))
        print(''.join(new_line).rstrip(), file=out)
    return out.getvalue()


def print_tile(location: Location, trails: TrailsMap):
    tile = location.get_contents(trails.tiles)
    if tile == '.':
        if location in trails.trail_by_loc:
            trail = trails.trail_by_loc[location]
            return label_for_index(trail.number)
        if location in trails.junction_by_loc:
            junction = trails.junction_by_loc[location]
            return str(junction.number % 10)
    elif tile == '#':
        return ' '
    return tile


def label_for_index(index):
    letter_index = index % 26
    return chr(ord('A') + letter_index)

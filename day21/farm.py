from dataclasses import dataclass
from itertools import chain


@dataclass(frozen=True)
class Location:
    x: int
    y: int

    def adjacent_tiles(self):
        return [
            Location(self.x - 1, self.y),
            Location(self.x + 1, self.y),
            Location(self.x, self.y - 1),
            Location(self.x, self.y + 1)
        ]

    def traverse_adjacent(self, traverse):
        return filter(lambda loc: loc is not None,
                      map(traverse, self.adjacent_tiles()))


@dataclass(frozen=True)
class FarmMap:
    lines: list[list[str]]
    start: Location
    width: int
    height: int

    def count_tiles_reachable(self, steps, wrap=False):
        if wrap:
            traverse = self.wrapping_traverse
        else:
            traverse = self.traverse
        locations = [self.start]
        for step in range(0, steps):
            locations = set(chain.from_iterable(
                map(lambda location: location.traverse_adjacent(traverse),
                    locations)
            ))
        return len(locations)

    def traverse(self, location):
        if location.x < 0 or location.x >= self.width:
            return None
        if location.y < 0 or location.y >= self.height:
            return None
        contents = self.lines[location.y][location.x]
        if contents != '#':
            return location
        else:
            return None

    def wrapping_traverse(self, location):
        x = location.x % self.width
        y = location.y % self.height
        contents = self.lines[y][x]
        if contents != '#':
            return location
        else:
            return None


def farm_from_list_of_lists(lines):
    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            if tile == 'S':
                return FarmMap(lines, Location(x, y), len(lines[0]), len(lines))
    return None

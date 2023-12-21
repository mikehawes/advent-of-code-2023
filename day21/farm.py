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


@dataclass(frozen=True)
class FarmMap:
    lines: list[list[str]]
    start: Location
    width: int
    height: int

    def count_tiles_reachable(self, steps):
        locations = [self.start]
        for step in range(0, steps):
            locations = self.next_locations(locations)
        return len(locations)

    def next_locations(self, locations):
        return set(chain.from_iterable(map(self.next_locations_single, locations)))

    def next_locations_single(self, location):
        return filter(self.is_traversable, location.adjacent_tiles())

    def is_traversable(self, location):
        if location.x < 0 or location.x >= self.width:
            return False
        if location.y < 0 or location.y >= self.height:
            return False
        contents = self.lines[location.y][location.x]
        return contents != '#'


def farm_from_list_of_lists(lines):
    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            if tile == 'S':
                return FarmMap(lines, Location(x, y), len(lines[0]), len(lines))
    return None

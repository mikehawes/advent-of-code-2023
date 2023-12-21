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

    def count_tiles_reachable(self, steps):
        locations = [self.start]
        for step in range(0, steps):
            locations = self.next_locations(locations)
        return len(locations)

    def next_locations(self, locations):
        return list(chain.from_iterable(map(self.next_locations_single, locations)))

    def next_locations_single(self, location):
        return []


def farm_from_list_of_lists(lines):
    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            if tile == 'S':
                return FarmMap(lines, Location(x, y))
    return None

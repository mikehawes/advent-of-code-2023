from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    x: int
    y: int

    def get_contents(self, tiles: list[list[str]]):
        if self.y < 0 or self.y >= len(tiles):
            return None
        line = tiles[self.y]
        if self.x < 0 or self.x >= len(line):
            return None
        return line[self.x]

    def plus(self, x=0, y=0):
        return Location(self.x + x, self.y + y)


@dataclass(frozen=True)
class Trail:
    number: int
    locations: list[Location]


@dataclass(frozen=True)
class TrailsMap:
    tiles: list[list[str]]
    trails: list[Trail]
    trail_by_loc: dict[Location, Trail]

    @staticmethod
    def from_lists(tiles: list[list[str]]):
        trails = find_trails(tiles)
        return TrailsMap(tiles, trails, index_trail_by_location(trails))

    @staticmethod
    def from_file(input_file):
        with open(input_file, 'r') as file:
            return TrailsMap.from_lists(list(map(lambda line: list(line.strip()), file)))


def find_trails(tiles: list[list[str]]):
    visited = {}
    visit = [Location(1, 0)]
    trails = []
    trail_number = 0
    while visit:
        trail = []
        next_on_trail = [visit.pop()]
        while len(next_on_trail) == 1:
            location = next_on_trail[0]
            trail.append(location)
            visited[location] = True
            next_on_trail = get_next(location, tiles, visited)
        trails.append(Trail(trail_number, trail))
        trail_number += 1
        if next_on_trail:
            visit.extend(next_on_trail)
    return trails


def get_next(current: Location, tiles: list[list[str]], visited: dict[Location, bool]):
    return list(filter(lambda loc: loc is not None,
                       map(lambda item: follow_next(current, item, tiles, visited),
                           [(lambda loc: loc.plus(x=-1), '<'), (lambda loc: loc.plus(x=1), '>'),
                            (lambda loc: loc.plus(y=-1), '^'), (lambda loc: loc.plus(y=1), 'v')])))


def follow_next(current: Location, item, tiles: list[list[str]], visited: dict[Location, bool]):
    next_in_direction, permitted_ramp = item
    location = next_in_direction(current)
    if location in visited:
        return None
    contents = location.get_contents(tiles)
    if contents == '.' or contents == permitted_ramp:
        return location
    else:
        return None


def index_trail_by_location(trails: list[Trail]):
    index = {}
    for trail in trails:
        for location in trail.locations:
            index[location] = trail
    return index

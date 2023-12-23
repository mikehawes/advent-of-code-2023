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
class Junction:
    number: int
    location: Location
    attached: list[Location]
    entrances: list[Location]
    exits: list[Location]

    @staticmethod
    def at_tile(number: int, location: Location, tiles: list[list[str]]):
        attached = []
        entrances = []
        exits = []
        for attached_location, outward_ramp, inward_ramp in [
            (location.plus(x=-1), '<', '>'), (location.plus(x=1), '>', '<'),
            (location.plus(y=-1), '^', 'v'), (location.plus(y=1), 'v', '^')]:
            contents = attached_location.get_contents(tiles)
            if contents != '#':
                attached.append(attached_location)
            if contents == '.':
                entrances.append(attached_location)
                exits.append(attached_location)
            elif contents == outward_ramp:
                exits.append(attached_location)
            elif contents == inward_ramp:
                entrances.append(attached_location)
        return Junction(number, location, attached, entrances, exits)

    def exits_from(self, location):
        return list(filter(lambda loc: loc != location, self.exits))


@dataclass(frozen=True)
class Trail:
    number: int
    locations: list[Location]
    start: Junction
    end: Junction


@dataclass(frozen=True)
class TrailsMap:
    tiles: list[list[str]]
    width: int
    height: int
    trails: list[Trail]
    trail_by_loc: dict[Location, Trail]
    junction_by_loc: dict[Location, Junction]

    @staticmethod
    def from_lists(tiles: list[list[str]]):
        trails, junctions_by_loc = find_trails_and_junctions(tiles)
        return TrailsMap(tiles, len(tiles[0]), len(tiles),
                         trails, index_trail_by_location(trails), junctions_by_loc)

    @staticmethod
    def from_file(input_file):
        with open(input_file, 'r') as file:
            return TrailsMap.from_lists(list(map(lambda line: list(line.strip()), file)))

    def all_from_junction(self, junction):
        return map(lambda loc: self.trail_by_loc[loc], junction.exits)


def find_trails_and_junctions(tiles: list[list[str]]):
    visited = {}
    start = Junction.at_tile(0, Location(1, 0), tiles)
    visit = [(start, Location(1, 1))]
    trails = []
    junctions_by_loc = {start.location: start}
    trail_number = 0
    junction_number = 1
    while visit:
        trail = []
        junction_before_trail, trail_start = visit.pop()
        last_location = junction_before_trail.location
        location = trail_start
        while location:
            if location in junctions_by_loc:
                junction = junctions_by_loc[location]
            else:
                junction = Junction.at_tile(junction_number, location, tiles)
            exits = junction.exits_from(last_location)
            if len(junction.attached) > 2 or not exits:
                if location not in junctions_by_loc:
                    junctions_by_loc[location] = junction
                    junction_number += 1
                visited[location] = True
                trails.append(Trail(trail_number, trail, junction_before_trail, junction))
                trail_number += 1
                visit.extend(map(lambda loc: (junction, loc),
                                 filter(lambda loc: loc not in visited,
                                        exits)))
                location = None
            else:
                visited[location] = True
                trail.append(location)
                last_location = location
                location = exits[0]
    return trails, junctions_by_loc


def index_trail_by_location(trails: list[Trail]):
    index = {}
    for trail in trails:
        for location in trail.locations:
            index[location] = trail
    return index

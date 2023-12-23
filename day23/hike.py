from dataclasses import dataclass
from itertools import chain

from day23.map import TrailsMap, Trail, Location, Junction


@dataclass(frozen=True)
class Hike:
    trails: TrailsMap
    start: Junction
    end: Junction
    route: list[Trail]
    visited_junction_numbers: frozenset[int]
    visited_locations: list[Location]

    @staticmethod
    def start_from(trails: TrailsMap, start: Junction, trail: Trail):
        route = [trail]
        return Hike(trails, start, trail.other_end_from(start), route,
                    find_visited_junction_numbers(start, route),
                    find_visited_locations(start, route))

    def extend_with_all_options(self):
        return list(map(self.extend_with,
                        filter(lambda trail: trail.other_end_from(self.end).number not in self.visited_junction_numbers,
                               self.trails.all_from_junction(self.end))))

    def extend_with(self, trail):
        return Hike(self.trails, self.start, trail.other_end_from(self.end),
                    list(chain(self.route, [trail])),
                    frozenset(chain(self.visited_junction_numbers, [trail.other_end_from(self.end).number])),
                    self.visited_locations + trail.locations_from(self.end))

    def steps(self):
        return len(self.visited_locations) - 1


def find_longest_hike(trails: TrailsMap) -> Hike:
    start = trails.junction_by_loc[Location(1, 0)]
    end = trails.junction_by_loc[Location(trails.width - 2, trails.height - 1)]
    hike = Hike.start_from(trails, start, next(trails.all_from_junction(start)))
    options = [hike]
    max_length = 0
    longest_hike = hike
    possible_hikes = 0
    hikes_to_end = 0
    while options:
        hike = options.pop()
        possible_hikes += 1
        if hike.end.number == end.number:
            hikes_to_end += 1
            hike_length = hike.steps()
            if hike_length > max_length:
                longest_hike = hike
                max_length = hike_length
        else:
            options.extend(hike.extend_with_all_options())
    print('Found {} possible hikes, {} to the end'.format(possible_hikes, hikes_to_end))
    return longest_hike


def find_visited_junction_numbers(start: Junction, route: list[Trail]) -> frozenset[int]:
    junction = start
    numbers = [junction.number]
    for trail in route:
        junction = trail.other_end_from(junction)
        numbers.append(junction.number)
    return frozenset(numbers)


def find_visited_locations(start: Junction, route: list[Trail]) -> list[Location]:
    junction = start
    locations = [junction.location]
    for trail in route:
        locations.extend(trail.locations_from(junction))
        junction = trail.other_end_from(junction)
    return locations

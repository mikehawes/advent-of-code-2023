from dataclasses import dataclass
from itertools import chain

from day23.map import TrailsMap, Trail, Location, Junction


@dataclass(frozen=True)
class Hike:
    trails: TrailsMap
    route: list[Trail]
    visited_junction_numbers: frozenset[int]
    visited_locations: list[Location]

    @staticmethod
    def from_route(trails: TrailsMap, route: list[Trail]):
        return Hike(trails, route, find_visited_junction_numbers(route), find_visited_locations(route))

    def extend_with_all_options(self):
        end = self.end()
        return list(map(self.extend_with,
                        filter(lambda trail: trail.end.number not in self.visited_junction_numbers,
                               self.trails.all_from_junction(end))))

    def extend_with(self, trail):
        return Hike(self.trails,
                    list(chain(self.route, [trail])),
                    frozenset(chain(self.visited_junction_numbers, [trail.end.number])),
                    self.visited_locations + trail.locations + [trail.end.location])

    def start(self) -> Junction:
        return self.route[0].start

    def end(self) -> Junction:
        return self.route[-1].end

    def steps(self):
        return len(self.visited_locations) - 1


def find_longest_hike(trails: TrailsMap) -> Hike:
    start = trails.junction_by_loc[Location(1, 0)]
    end = trails.junction_by_loc[Location(trails.width - 2, trails.height - 1)]
    hike = Hike.from_route(trails, list(trails.all_from_junction(start)))
    options = [hike]
    max_length = 0
    longest_hike = hike
    possible_hikes = 0
    hikes_to_end = 0
    while options:
        hike = options.pop()
        possible_hikes += 1
        if hike.end().number == end.number:
            hikes_to_end += 1
            hike_length = hike.steps()
            if hike_length > max_length:
                longest_hike = hike
                max_length = hike_length
        else:
            options.extend(hike.extend_with_all_options())
    print('Found {} possible hikes, {} to the end'.format(possible_hikes, hikes_to_end))
    return longest_hike


def find_visited_junction_numbers(route: list[Trail]) -> frozenset[int]:
    return frozenset(map(lambda junction: junction.number,
                         chain([route[0].start],
                               map(lambda trail: trail.end, route))))


def find_visited_locations(route: list[Trail]) -> list[Location]:
    locations = [route[0].start.location]
    for trail in route:
        locations.extend(trail.locations)
        locations.append(trail.end.location)
    return locations

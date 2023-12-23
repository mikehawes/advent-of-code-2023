from dataclasses import dataclass

from day23.map import TrailsMap, Trail, Location


@dataclass
class Hike:
    trails: TrailsMap
    route: list[Trail]


def find_longest_hike(trails: TrailsMap) -> Hike:
    start = trails.junction_by_loc[Location(1, 0)]
    route = []
    return Hike(trails, route)

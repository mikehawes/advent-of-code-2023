from dataclasses import dataclass

from day22.brick import SandBrick, Size, Location


@dataclass(frozen=True)
class BricksSnapshot:
    bricks: list[SandBrick]
    bricks_by_location: dict[Location, SandBrick]
    size: Size

    @staticmethod
    def from_list(bricks: list[SandBrick]):
        return BricksSnapshot(bricks, index_brick_locations(bricks), find_snapshot_size(bricks))


def find_snapshot_size(bricks: list[SandBrick]) -> Size:
    max_x = 0
    max_y = 0
    max_z = 0
    for brick in bricks:
        loc = brick.max_location()
        max_x = max(loc.x, max_x)
        max_y = max(loc.y, max_y)
        max_z = max(loc.z, max_z)
    return Size(max_x, max_y, max_z)


def index_brick_locations(bricks: list[SandBrick]) -> dict[Location, SandBrick]:
    locations = {}
    for brick in bricks:
        for location in brick.locations_covered():
            locations[location] = brick
    return locations

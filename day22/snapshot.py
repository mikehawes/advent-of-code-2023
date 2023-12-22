from dataclasses import dataclass, replace

from day22.brick import SandBrick, Size, Location


@dataclass(frozen=True)
class BricksSnapshot:
    bricks: list[SandBrick]
    bricks_by_location: dict[Location, SandBrick]
    bricks_by_min_z: dict[int, list[SandBrick]]
    size: Size

    @staticmethod
    def from_list(bricks: list[SandBrick]):
        return BricksSnapshot(bricks,
                              index_brick_locations(bricks),
                              index_bricks_by_min_z(bricks),
                              find_snapshot_size(bricks))

    def settle(self):
        bricks = []
        bricks_by_location = {}
        for z in range(1, self.size.z):
            if z not in self.bricks_by_min_z:
                continue
            for brick in self.bricks_by_min_z[z]:
                new_brick = brick
                for z2 in range(z - 1, 0, -1):
                    potential = replace(brick, location=replace(brick.location, z=z2))
                    any_overlap = any(overlapping_bricks(potential, bricks_by_location))
                    if not any_overlap:
                        new_brick = potential
                    else:
                        break
                bricks.append(new_brick)
                for location in new_brick.locations_covered():
                    bricks_by_location[location] = new_brick
        return BricksSnapshot.from_list(bricks)

    def count_disintegratable_bricks(self):
        above_by_brick_loc = {}
        below_by_brick_loc = {}
        for brick in self.bricks:
            below = replace(brick, location=replace(brick.location, z=brick.location.z - 1))
            below_bricks = list(filter(lambda b: b != brick,
                                       overlapping_bricks(below, self.bricks_by_location)))
            below_by_brick_loc[brick.location] = below_bricks
            for below_brick in below_bricks:
                loc = below_brick.location
                if loc in above_by_brick_loc:
                    above_by_brick_loc[loc].append(brick)
                else:
                    above_by_brick_loc[loc] = [brick]

        disintegratabale_count = 0
        for brick in self.bricks:
            disintegratable = True
            if brick.location in above_by_brick_loc:
                for above in above_by_brick_loc[brick.location]:
                    if len(below_by_brick_loc[above.location]) == 1:
                        disintegratable = False
                        break
            if disintegratable:
                disintegratabale_count += 1

        return disintegratabale_count


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


def index_bricks_by_min_z(bricks: list[SandBrick]) -> dict[int, list[SandBrick]]:
    by_z = {}
    for brick in bricks:
        min_z = brick.min_z()
        if min_z not in by_z:
            by_z[min_z] = [brick]
        else:
            by_z[min_z].append(brick)
    return by_z


def overlapping_bricks(brick, bricks_by_location):
    bricks = {}
    for location in brick.locations_covered():
        if location not in bricks_by_location:
            continue
        found_brick = bricks_by_location[location]
        bricks[found_brick] = True
    return bricks.keys()

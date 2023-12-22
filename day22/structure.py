from dataclasses import replace, dataclass
from itertools import chain

from day22.brick import SandBrick, Location
from day22.snapshot import BricksSnapshot


@dataclass(frozen=True)
class SupportStructure:
    snapshot: BricksSnapshot
    above_by_brick_loc: dict[Location, list[SandBrick]]
    below_by_brick_loc: dict[Location, list[SandBrick]]

    @staticmethod
    def from_snapshot(snapshot: BricksSnapshot):
        above_by_brick_loc = {}
        below_by_brick_loc = {}
        for brick in snapshot.bricks:
            below = replace(brick, location=replace(brick.location, z=brick.location.z - 1))
            below_bricks = list(filter(lambda b: b != brick,
                                       snapshot.overlapping_bricks(below)))
            below_by_brick_loc[brick.location] = below_bricks
            for below_brick in below_bricks:
                loc = below_brick.location
                if loc in above_by_brick_loc:
                    above_by_brick_loc[loc].append(brick)
                else:
                    above_by_brick_loc[loc] = [brick]
        return SupportStructure(snapshot, above_by_brick_loc, below_by_brick_loc)

    def count_disintegratable_bricks(self):
        disintegratable_count = 0
        for brick in self.snapshot.bricks:
            if self.is_disintegratable(brick):
                disintegratable_count += 1
        return disintegratable_count

    def is_disintegratable(self, brick):
        if brick.location in self.above_by_brick_loc:
            for above in self.above_by_brick_loc[brick.location]:
                if len(self.below_by_brick_loc[above.location]) == 1:
                    return False
        return True

    def total_would_fall_for_each_brick(self):
        total = 0
        for brick in self.snapshot.bricks:
            would_fall = self.which_bricks_would_fall(brick)
            total += len(would_fall)
        return total

    def which_bricks_would_fall(self, brick):
        result = {}
        self.add_bricks_would_fall([brick], result)
        return result

    def add_bricks_would_fall(self, remove_bricks, result):
        locations = set(map(lambda brick: brick.location, remove_bricks))
        above_bricks = chain.from_iterable(
            map(lambda brick: self.above_by_brick_loc[brick.location],
                filter(lambda brick: brick.location in self.above_by_brick_loc,
                       remove_bricks)))
        supported_bricks = list(filter(lambda brick: all(map(lambda below: below.location in locations,
                                                             self.below_by_brick_loc[brick.location])),
                                       above_bricks))
        if not supported_bricks:
            return
        for supported in supported_bricks:
            result[supported.location] = True
        self.add_bricks_would_fall(supported_bricks, result)

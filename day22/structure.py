from dataclasses import dataclass
from itertools import chain

from day22.brick import SandBrick
from day22.snapshot import BricksSnapshot


@dataclass(frozen=True)
class SupportStructure:
    snapshot: BricksSnapshot
    above_by_brick: dict[int, list[SandBrick]]
    below_by_brick: dict[int, list[SandBrick]]

    @staticmethod
    def from_snapshot(snapshot: BricksSnapshot):
        above_by_brick = {}
        below_by_brick = {}
        for brick in snapshot.bricks:
            below = brick.plus_location(z=-1)
            below_bricks = list(filter(lambda b: b != brick,
                                       snapshot.overlapping_bricks(below)))
            below_by_brick[brick.index] = below_bricks
            for below_brick in below_bricks:
                index = below_brick.index
                if index in above_by_brick:
                    above_by_brick[index].append(brick)
                else:
                    above_by_brick[index] = [brick]
        return SupportStructure(snapshot, above_by_brick, below_by_brick)

    def which_bricks_would_fall(self, brick):
        result = {}
        bricks = [brick]
        while bricks:
            bricks = self.which_of_above_would_fall(bricks)
            for brick in bricks:
                result[brick.location] = True
        return result.keys()

    def which_of_above_would_fall(self, remove_bricks):
        locations = set(map(lambda brick: brick.location, remove_bricks))
        return list(filter(lambda brick: all(map(lambda below: below.location in locations,
                                                 self.below_brick_or_fail(brick))),
                           self.above_bricks(remove_bricks)))

    def above_bricks(self, bricks):
        return set(chain.from_iterable(map(self.above_brick, bricks)))

    def above_brick(self, brick):
        if brick.index in self.above_by_brick:
            return self.above_by_brick[brick.index]
        else:
            return []

    def below_brick(self, brick):
        if brick.index in self.below_by_brick:
            return self.below_by_brick[brick.index]
        else:
            return []

    def below_brick_or_fail(self, brick):
        return self.below_by_brick[brick.index]

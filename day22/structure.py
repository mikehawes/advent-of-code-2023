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
        would_fall = []
        bricks = [brick]
        while bricks:
            bricks = self.which_of_above_would_fall(bricks)
            would_fall.extend(bricks)
        return would_fall

    def which_of_above_would_fall(self, remove_bricks):
        remove_indexes = set(map(lambda brick: brick.index, remove_bricks))
        would_fall = {}
        for remove_brick in remove_bricks:
            for above in self.above_brick(remove_brick):
                fall = True
                for below in self.below_brick(above):
                    if below.index not in remove_indexes:
                        fall = False
                if fall:
                    if above.index not in would_fall:
                        would_fall[above.index] = above
        return would_fall.values()

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

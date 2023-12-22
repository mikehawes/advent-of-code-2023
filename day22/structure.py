from dataclasses import replace, dataclass

from day22.brick import SandBrick, Location


@dataclass(frozen=True)
class SupportStructure:
    above_by_brick_loc: dict[Location, list[SandBrick]]
    below_by_brick_loc: dict[Location, list[SandBrick]]

    @staticmethod
    def from_snapshot(snapshot):
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
        return SupportStructure(above_by_brick_loc, below_by_brick_loc)

    def is_disintegratable(self, brick):
        if brick.location in self.above_by_brick_loc:
            for above in self.above_by_brick_loc[brick.location]:
                if len(self.below_by_brick_loc[above.location]) == 1:
                    return False
        return True

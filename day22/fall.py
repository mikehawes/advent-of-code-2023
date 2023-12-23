from dataclasses import dataclass

from day22.brick import SandBrick
from day22.snapshot import BricksSnapshot
from day22.structure import SupportStructure


@dataclass(frozen=True)
class WhichBricksWouldFall:
    snapshot: BricksSnapshot
    would_fall_by_index: dict[int, list[SandBrick]]

    @staticmethod
    def from_structure(structure: SupportStructure):
        would_fall_by_index = {}
        for brick in structure.snapshot.bricks:
            would_fall_by_index[brick.index] = list(structure.which_bricks_would_fall(brick))
        return WhichBricksWouldFall(structure.snapshot, would_fall_by_index)

    @staticmethod
    def from_snapshot(snapshot: BricksSnapshot):
        return WhichBricksWouldFall.from_structure(
            SupportStructure.from_snapshot(snapshot))

    def count_disintegratable_bricks(self):
        disintegratable_count = 0
        for brick in self.snapshot.bricks:
            if self.is_disintegratable(brick):
                disintegratable_count += 1
        return disintegratable_count

    def is_disintegratable(self, brick):
        return not self.which_bricks_would_fall(brick)

    def total_would_fall_for_each_brick(self):
        total = 0
        for brick in self.snapshot.bricks:
            would_fall = self.which_bricks_would_fall(brick)
            total += len(would_fall)
        return total

    def max_would_fall_for_brick(self):
        max_fall = 0
        max_brick = None
        for brick in self.snapshot.bricks:
            would_fall = self.which_bricks_would_fall(brick)
            num_fall = len(would_fall)
            if num_fall > max_fall:
                max_fall = num_fall
                max_brick = brick
        return max_fall, max_brick

    def which_bricks_would_fall(self, brick):
        return self.would_fall_by_index[brick.index]

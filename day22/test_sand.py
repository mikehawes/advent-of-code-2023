import unittest

from approvaltests import verify

from day22.brick import Location, SandBrick, Size
from day22.input import load_bricks_from_file
from day22.sand_printer import print_bricks_snapshot
from day22.snapshot import BricksSnapshot
from day22.structure import SupportStructure


class TestSand(unittest.TestCase):

    def test_should_print_snapshot_for_example(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('example'))
        verify(print_bricks_snapshot(snapshot))

    def test_should_settle_snapshot_for_example(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('example'))
        verify(print_bricks_snapshot(snapshot.settle()))

    def test_should_view_layers_for_example(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('example'))
        verify(print_bricks_snapshot(snapshot.settle(), layers=True))

    def test_should_print_snapshot_for_input(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('input'))
        verify(print_bricks_snapshot(snapshot))

    def test_should_settle_snapshot_for_input(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('input'))
        verify(print_bricks_snapshot(snapshot.settle()))

    def test_should_view_layers_for_input(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('input'))
        verify(print_bricks_snapshot(snapshot.settle(), layers=True))

    def test_should_count_disintegratable_bricks_for_example(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('example')).settle()
        structure = SupportStructure.from_snapshot(snapshot)
        self.assertEqual(5, structure.count_disintegratable_bricks())

    def test_should_count_disintegratable_bricks_for_input(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('input')).settle()
        structure = SupportStructure.from_snapshot(snapshot)
        self.assertEqual(375, structure.count_disintegratable_bricks())

    def test_should_total_would_fall_for_each_brick_for_example(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('example')).settle()
        structure = SupportStructure.from_snapshot(snapshot)
        self.assertEqual(7, structure.total_would_fall_for_each_brick())

    def test_should_total_would_fall_for_each_brick_for_input(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('input')).settle()
        structure = SupportStructure.from_snapshot(snapshot)
        self.assertEqual(66923, structure.total_would_fall_for_each_brick())  # Too low!

    def test_should_find_max_would_fall_for_a_brick_for_input(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('input')).settle()
        structure = SupportStructure.from_snapshot(snapshot)
        would_fall, brick = structure.max_would_fall_for_brick()
        self.assertEqual([1018, SandBrick(Location(5, 5, 8), Size(x=3), index=325)],
                         [would_fall, brick])

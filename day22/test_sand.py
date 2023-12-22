import unittest

from approvaltests import verify

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

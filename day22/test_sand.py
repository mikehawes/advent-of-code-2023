import unittest

from approvaltests import verify

from day22.input import load_bricks_from_file
from day22.sand_printer import print_bricks_snapshot
from day22.snapshot import BricksSnapshot


class TestSand(unittest.TestCase):

    def test_should_print_snapshot_for_example(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('example'))
        verify(print_bricks_snapshot(snapshot))

    def test_should_settle_snapshot_for_example(self):
        snapshot = BricksSnapshot.from_list(load_bricks_from_file('example'))
        verify(print_bricks_snapshot(snapshot.settle()))

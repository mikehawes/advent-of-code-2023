import unittest

from approvaltests import verify

from day21.farm_printer import print_reachable_counts
from day21.input import read_farm_map_from_file


class TestFarm(unittest.TestCase):

    def test_should_count_tiles_reachable_for_example(self):
        farm = read_farm_map_from_file('example')
        verify(print_reachable_counts(farm, [6, 10, 50]))

    def test_should_count_tiles_reachable_for_input(self):
        farm = read_farm_map_from_file('input')
        self.assertEqual(3651, farm.count_tiles_reachable(steps=64))

    def test_should_count_tiles_reachable_for_example_with_wrapping(self):
        farm = read_farm_map_from_file('example')
        verify(print_reachable_counts(farm, [6, 10, 50, 100], wrap=True))

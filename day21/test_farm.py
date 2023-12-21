import unittest

from day21.input import read_farm_map_from_file


class TestFarm(unittest.TestCase):

    def test_should_count_tiles_reachable_for_example(self):
        farm = read_farm_map_from_file('example')
        self.assertEqual(16, farm.count_tiles_reachable(steps=6))

    def test_should_count_tiles_reachable_for_input(self):
        farm = read_farm_map_from_file('input')
        self.assertEqual(3651, farm.count_tiles_reachable(steps=64))

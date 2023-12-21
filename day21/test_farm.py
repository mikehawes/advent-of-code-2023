import unittest

from day21.input import read_farm_map_from_file


class TestFarm(unittest.TestCase):

    @unittest.skip('TODO')
    def test_should_count_tiles_reachable_for_example(self):
        farm = read_farm_map_from_file('example')
        self.assertEqual(16, farm.count_tiles_reachable(steps=6))

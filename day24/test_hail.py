import unittest

from day24.collision import count_2d_collisions_in_area
from day24.hail import load_hailstones_from_file, Position


class TestHail(unittest.TestCase):

    @unittest.skip('TODO')
    def test_should_count_2d_path_intersections_for_example(self):
        hailstones = load_hailstones_from_file('example')
        self.assertEqual(2, count_2d_collisions_in_area(hailstones, Position.all(7), Position.all(27)))

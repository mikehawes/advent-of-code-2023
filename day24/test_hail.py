import unittest

from approvaltests import verify

from day24.collision import count_2d_intersections_in_area
from day24.collision_printer import print_2d_intersections
from day24.hail import load_hailstones_from_file, Position


class TestHail(unittest.TestCase):

    def test_should_list_2d_path_intersections_for_example(self):
        hailstones = load_hailstones_from_file('example')
        verify(print_2d_intersections(hailstones))

    def test_should_count_2d_path_intersections_for_example(self):
        self.assertEqual(2, count_2d_intersections_in_area(
            load_hailstones_from_file('example'), Position.all(7), Position.all(27)))

    def test_should_count_2d_path_intersections_for_input(self):
        self.assertEqual(18098, count_2d_intersections_in_area(
            load_hailstones_from_file('input'), Position.all(200000000000000), Position.all(400000000000000)))

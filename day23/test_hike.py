import unittest

from approvaltests import verify

from day23.hike import find_longest_hike
from day23.hike_printer import print_trails_map, print_hike
from day23.map import TrailsMap


class TestHike(unittest.TestCase):

    def test_should_print_example_map(self):
        trails = TrailsMap.from_file('example')
        verify(print_trails_map(trails))

    def test_should_find_longest_hike_in_example(self):
        trails = TrailsMap.from_file('example')
        verify(print_hike(find_longest_hike(trails)))

    def test_should_find_longest_hike_in_input(self):
        trails = TrailsMap.from_file('input')
        verify(print_hike(find_longest_hike(trails)))

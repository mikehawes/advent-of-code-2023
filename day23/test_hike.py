import unittest

from approvaltests import verify

from day23.hike_printer import print_trails_map
from day23.map import TrailsMap


class TestHike(unittest.TestCase):

    def test_should_find_longest_hike_in_example(self):
        trails = TrailsMap.from_file('example')
        verify(print_trails_map(trails))

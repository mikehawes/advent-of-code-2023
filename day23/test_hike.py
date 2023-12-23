import unittest

from approvaltests import verify

from day23.hike_printer import print_trails_map
from day23.input import read_trails_from_file


class TestHike(unittest.TestCase):

    def test_should_find_longest_hike_in_example(self):
        trails = read_trails_from_file('example')
        verify(print_trails_map(trails))

import unittest

from day6.day6p1 import multiply_ways_to_beat
from day6.day6p2 import ways_to_beat_multiplied_race


class TestDay6Part1(unittest.TestCase):

    def test_should_multiply_ways_to_beat_example_distances(self):
        self.assertEqual(288, multiply_ways_to_beat('example'))

    def test_should_multiply_ways_to_beat_input_distances(self):
        self.assertEqual(500346, multiply_ways_to_beat('input'))


class TestDay6Part2(unittest.TestCase):

    def test_should_multiply_ways_to_beat_example_distances(self):
        self.assertEqual(71503, ways_to_beat_multiplied_race('example'))

    def test_should_multiply_ways_to_beat_input_distances(self):
        self.assertEqual(42515755, ways_to_beat_multiplied_race('input'))

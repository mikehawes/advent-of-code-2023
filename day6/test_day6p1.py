import unittest

from day6.day6p1 import multiply_ways_to_beat, get_button_press_times, count_winning_options


class TestDay6Part1(unittest.TestCase):

    def test_should_get_first_example_race_button_press_time(self):
        self.assertEqual([1.6972243622680054, 5.302775637731995], get_button_press_times(7, 9))

    def test_should_count_ways_to_beat_first_example_race(self):
        self.assertEqual(4, count_winning_options(7, 9))

    def test_should_get_second_example_race_button_press_time(self):
        self.assertEqual([3.4688711258507254, 11.531128874149275], get_button_press_times(15, 40))

    def test_should_count_ways_to_beat_second_example_race(self):
        self.assertEqual(8, count_winning_options(15, 40))

    def test_should_get_third_example_race_button_press_time(self):
        self.assertEqual([10.0, 20.0], get_button_press_times(30, 200))

    def test_should_count_ways_to_beat_third_example_race(self):
        self.assertEqual(9, count_winning_options(30, 200))

    def test_should_multiply_ways_to_beat_example_distances(self):
        self.assertEqual(288, multiply_ways_to_beat('example'))

    def test_should_multiply_ways_to_beat_input_distances(self):
        self.assertEqual(500346, multiply_ways_to_beat('input'))

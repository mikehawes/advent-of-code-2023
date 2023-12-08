import unittest

from day8.day8p1 import count_steps_from_a_to_z


class TestDay8Part1(unittest.TestCase):

    def test_should_get_steps_for_example_1(self):
        self.assertEqual(2, count_steps_from_a_to_z('example1'))

    def test_should_get_steps_for_example_2(self):
        self.assertEqual(6, count_steps_from_a_to_z('example2'))

    def test_should_get_steps_for_input(self):
        self.assertEqual(23147, count_steps_from_a_to_z('input'))


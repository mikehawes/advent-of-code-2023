import unittest

from day08.day8p1 import count_steps_from_a_to_z
from day08.day8p2 import count_steps_from_a_to_z_as_ghost


class TestDay8Part1(unittest.TestCase):

    def test_should_get_steps_for_example_1(self):
        self.assertEqual(2, count_steps_from_a_to_z('example1'))

    def test_should_get_steps_for_example_2(self):
        self.assertEqual(6, count_steps_from_a_to_z('example2'))

    def test_should_get_steps_for_input(self):
        self.assertEqual(23147, count_steps_from_a_to_z('input'))


class TestDay8Part2(unittest.TestCase):

    def test_should_get_steps_for_example_3(self):
        self.assertEqual(6, count_steps_from_a_to_z_as_ghost('example3'))

    @unittest.skip('Takes about half an hour')
    def test_should_get_steps_for_input(self):
        self.assertEqual(22_289_513_667_691, count_steps_from_a_to_z_as_ghost('input'))

import unittest

from day16.mirrors import count_energized_tiles_in_file


class TestMirrors(unittest.TestCase):

    def test_should_count_energized_tiles_in_example(self):
        self.assertEqual(46, count_energized_tiles_in_file('example'))

    def test_should_count_energized_tiles_in_input(self):
        self.assertEqual(8539, count_energized_tiles_in_file('input'))

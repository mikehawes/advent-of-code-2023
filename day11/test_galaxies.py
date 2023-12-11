import unittest

from approvaltests import verify

from day11.galaxies import read_and_expand_space_from_file, sum_galaxy_distances_from_file


class TestGalaxies(unittest.TestCase):

    def test_should_expand_empty_space_in_example(self):
        verify('\n'.join(read_and_expand_space_from_file('example')))

    def test_should_sum_distances_in_example(self):
        self.assertEqual(374, sum_galaxy_distances_from_file('example'))

    def test_should_sum_distances_in_input(self):
        self.assertEqual(9684228, sum_galaxy_distances_from_file('input'))

    def test_should_sum_distances_in_example_with_larger_expansion(self):
        self.assertEqual(1030, sum_galaxy_distances_from_file('example', expansion=10))

    def test_should_sum_distances_in_input_with_larger_expansion(self):
        self.assertEqual(483844716556, sum_galaxy_distances_from_file('input', expansion=1000000))

import unittest

from approvaltests import verify

from day18.instruction import read_dig_instructions_from_file
from day18.part1 import dig_lagoon
from day18.part2 import compute_lagoon_capacity


class TestLagoon(unittest.TestCase):

    def test_should_dig_example_lagoon(self):
        instructions = read_dig_instructions_from_file('example')
        lagoon = dig_lagoon(instructions)
        verify(str(lagoon))

    def test_should_dig_input_lagoon(self):
        instructions = read_dig_instructions_from_file('input')
        lagoon = dig_lagoon(instructions)
        verify(str(lagoon))

    def test_should_compute_capacity_of_example_lagoon(self):
        instructions = read_dig_instructions_from_file('example')
        self.assertEqual(62, compute_lagoon_capacity(instructions))

    def test_should_compute_capacity_of_input_lagoon(self):
        instructions = read_dig_instructions_from_file('input')
        self.assertEqual(92758, compute_lagoon_capacity(instructions))

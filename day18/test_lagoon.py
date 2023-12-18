import unittest

from approvaltests import verify

from day18.capacity import compute_lagoon_capacity
from day18.instruction import read_dig_instructions_from_file, read_hex_dig_instructions_from_file
from day18.lagoon import dig_lagoon


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

    def test_should_compute_capacity_of_example_lagoon_from_hex_instructions(self):
        instructions = read_hex_dig_instructions_from_file('example')
        self.assertEqual(952408144115, compute_lagoon_capacity(instructions))

    def test_should_compute_capacity_of_input_lagoon_from_hex_instructions(self):
        instructions = read_hex_dig_instructions_from_file('input')
        self.assertEqual(62762509300678, compute_lagoon_capacity(instructions))

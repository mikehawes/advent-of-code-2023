import unittest

from approvaltests import verify

from day18.instruction import read_dig_instructions_from_file
from day18.lagoon import dig_lagoon


class TestLagoon(unittest.TestCase):

    def test_should_dig_example_lagoon(self):
        instructions = read_dig_instructions_from_file('example')
        lagoon = dig_lagoon(instructions)
        verify(str(lagoon))

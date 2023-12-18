import unittest

from approvaltests import verify

from day18.lagoon import read_dig_instructions_from_file


class TestLagoon(unittest.TestCase):

    def test_should_dig_example_lagoon(self):
        instructions = read_dig_instructions_from_file('example')
        verify('\n'.join(map(str, instructions)))

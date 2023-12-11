import unittest

from approvaltests import verify

from day11.galaxies import read_and_expand_space_from_file


class TestGalaxies(unittest.TestCase):

    def test_should_expand_empty_space_in_example(self):
        verify('\n'.join(read_and_expand_space_from_file('example')))

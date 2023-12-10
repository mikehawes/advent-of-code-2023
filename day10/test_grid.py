import unittest

from approvaltests import verify

from day10.grid import read_grid_from_file
from day10.grid_printer import print_grid


class TestGrid(unittest.TestCase):

    def test_should_read_grid_for_example1(self):
        grid = read_grid_from_file('example1')
        verify(print_grid(grid))

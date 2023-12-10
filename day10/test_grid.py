import unittest

from day10.grid import read_grid_from_file
from day10.grid_printer import print_grid, print_node


class TestGrid(unittest.TestCase):

    def test_should_read_grid_for_example1(self):
        grid = read_grid_from_file('example1')
        self.assertEquals(open('example1', 'r').read(),
                          print_grid(grid))

    def test_should_find_start_for_example1(self):
        grid = read_grid_from_file('example1')
        self.assertEquals('S at 1,1',
                          print_node(grid.start_node()))

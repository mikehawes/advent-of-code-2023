import unittest

from approvaltests import verify

from day17.crucible import load_grid_from_file
from day17.grid_printer import print_path


class TestCrucible(unittest.TestCase):
    def test_should_find_path_in_example(self):
        grid = load_grid_from_file('example')
        path = grid.find_path(grid.top_left(), grid.bottom_right())
        verify(print_path(grid, path))

    def test_should_find_path_in_input(self):
        grid = load_grid_from_file('input')
        path = grid.find_path(grid.top_left(), grid.bottom_right())
        verify(print_path(grid, path))

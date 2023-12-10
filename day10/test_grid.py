import unittest

from approvaltests import verify

from day10.grid import read_grid_from_file
from day10.grid_printer import print_answers


class TestGrid(unittest.TestCase):

    def test_should_answer_example1(self):
        grid = read_grid_from_file('example1')
        verify(print_answers(grid))

    def test_should_answer_example2(self):
        grid = read_grid_from_file('example2')
        verify(print_answers(grid))

    def test_should_answer_example3(self):
        grid = read_grid_from_file('example3')
        verify(print_answers(grid))

    def test_should_answer_example4(self):
        grid = read_grid_from_file('example4')
        verify(print_answers(grid))

    def test_should_answer_input(self):
        grid = read_grid_from_file('input')
        verify(print_answers(grid))

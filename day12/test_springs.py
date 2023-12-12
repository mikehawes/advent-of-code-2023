import unittest

from approvaltests import verify

from day12.springs_printer import print_working_spring_arrangements_for_file


class TestGalaxies(unittest.TestCase):

    def test_should_print_working_spring_arrangements_for_example(self):
        verify(print_working_spring_arrangements_for_file('example'))

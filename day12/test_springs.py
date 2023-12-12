import unittest

from approvaltests import verify

from day12.springs import SpringConditionRecord, total_spring_arrangements_from_file
from day12.springs_printer import print_working_spring_arrangements_for_file


class TestGalaxies(unittest.TestCase):

    def test_should_print_working_spring_arrangements_for_example(self):
        verify(print_working_spring_arrangements_for_file('example'))

    def test_should_count_arrangements_1(self):
        record = SpringConditionRecord("???.###", [1, 1, 3])
        self.assertEqual(1, record.arrangements().arrangements_count)

    def test_should_count_arrangements_2(self):
        record = SpringConditionRecord("?.#??.??#?", [2, 1, 1])
        self.assertEqual(1, record.arrangements().arrangements_count)

    def test_should_print_working_spring_arrangements_for_input(self):
        verify(print_working_spring_arrangements_for_file('input'))

    def test_should_multiply_working_spring_arrangements_by_2_for_example(self):
        verify(print_working_spring_arrangements_for_file('example', multiple=2))

    def test_should_multiply_working_spring_arrangements_by_5_for_example(self):
        self.assertEqual(525152, total_spring_arrangements_from_file('example', multiple=5))

    def test_should_multiply_arrangements_1(self):
        record = SpringConditionRecord("???.###", [1, 1, 3])
        self.assertEqual(1, record.arrangements(multiple=2).arrangements_count)

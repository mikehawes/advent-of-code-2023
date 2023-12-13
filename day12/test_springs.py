import unittest

from approvaltests import verify

from day12.springs import SpringConditionRecord, total_spring_arrangements_from_file, read_spring_conditions_from_file, \
    total_spring_arrangements_from_records
from day12.springs_printer import print_working_spring_arrangements_for_file


class TestSprings(unittest.TestCase):

    def test_should_print_working_spring_arrangements_for_example(self):
        verify(print_working_spring_arrangements_for_file('example'))

    def test_should_count_arrangements_1(self):
        record = SpringConditionRecord("???.###", [1, 1, 3])
        self.assertEqual(1, record.count_arrangements())

    def test_should_count_arrangements_2(self):
        record = SpringConditionRecord("?.#??.??#?", [2, 1, 1])
        self.assertEqual(1, record.count_arrangements())

    def test_should_print_working_spring_arrangements_for_input(self):
        verify(print_working_spring_arrangements_for_file('input'))

    def test_should_multiply_working_spring_arrangements_by_2_for_example(self):
        verify(print_working_spring_arrangements_for_file('example', multiple=2))

    def test_should_multiply_working_spring_arrangements_by_numbers_for_example(self):
        records = read_spring_conditions_from_file('example')
        totals = list(map(lambda multiple: total_spring_arrangements_from_records(records, multiple),
                          [1, 2, 3, 4, 5]))
        self.assertEqual([21, 206, 2612, 36308, 525152], totals)

    def test_should_multiply_working_spring_arrangements_by_5_for_example(self):
        self.assertEqual(525152, total_spring_arrangements_from_file('example', multiple=5))

    @unittest.skip('Too slow')
    def test_should_multiply_working_spring_arrangements_by_6_for_example(self):
        self.assertEqual(7737356, total_spring_arrangements_from_file('example', multiple=6))

    @unittest.skip('Too slow')
    def test_should_multiply_working_spring_arrangements_by_5_for_input(self):
        self.assertEqual(0, total_spring_arrangements_from_file('input', multiple=5))

    def test_should_multiply_arrangements_1(self):
        record = SpringConditionRecord("???.###", [1, 1, 3])
        self.assertEqual(1, record.count_arrangements(multiple=2))

    def test_should_multiply_arrangements_2(self):
        record = SpringConditionRecord("..???.??.?", [1, 1, 1])
        counts = list(map(lambda multiple: record.count_arrangements(multiple=multiple),
                          [1, 2, 3, 4]))
        self.assertEqual([9, 226, 6360, 188_488], counts)

    def test_should_multiply_arrangements_3(self):
        record = SpringConditionRecord("..???.??.?", [1, 1, 1])
        self.assertEqual(5_752_544, record.count_arrangements(multiple=5))

    @unittest.skip('Too slow')
    def test_should_multiply_arrangements_4(self):
        record = SpringConditionRecord("?###????????", [3, 2, 1])
        self.assertEqual(7_593_750, record.count_arrangements(multiple=6))

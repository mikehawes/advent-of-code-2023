import unittest

from approvaltests import verify

from day12.springs import SpringConditionRecord, total_spring_arrangements_from_file, read_spring_conditions_from_file, \
    total_spring_arrangements_from_records
from day12.springs_printer import print_working_spring_arrangements_for_file, list_of_record_and_arrangement_count, \
    print_working_spring_arrangements_for_records


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

    def test_should_multiply_working_spring_arrangements_by_6_for_example(self):
        self.assertEqual(7_737_356, total_spring_arrangements_from_file('example', multiple=6))

    @unittest.skip('Too slow')
    def test_should_multiply_working_spring_arrangements_by_5_for_input(self):
        self.assertEqual(0, total_spring_arrangements_from_file('input', multiple=5))

    def test_should_multiply_arrangements_example_line_1(self):
        record = SpringConditionRecord("???.###", [1, 1, 3])
        self.assertEqual(1, record.count_arrangements(multiple=5))

    def test_should_multiply_arrangements_input_line_1(self):
        record = SpringConditionRecord("..???.??.?", [1, 1, 1])
        self.assertEqual(5_752_544, record.count_arrangements(multiple=5))

    def test_should_multiply_arrangements_input_line_24(self):
        record = SpringConditionRecord("??#?#?????????????.", [8, 4, 1])
        self.assertEqual(67_192_396, record.count_arrangements(multiple=5))


class TestSpringsInputLine41(unittest.TestCase):
    def setUp(self):
        self.records = [
            SpringConditionRecord("????#????.???", [1, 2, 1, 1]),
            SpringConditionRecord("????#????", [1, 2, 1, 1]),
            SpringConditionRecord("????#????", [1, 2, 1]),
            SpringConditionRecord("????#????", [1, 2]),
            SpringConditionRecord("???", [1]),
            SpringConditionRecord("???", [1, 1])
        ]
        self.partial_records = self.records[1:]
        self.record = self.records[0]

    @unittest.skip('Too slow')
    def test_should_find_arrangements_for_multiple_5(self):
        self.assertEqual(0, self.record.count_arrangements(multiple=5))

    def test_should_find_arrangements_for_partial_multiple_5(self):
        self.assertEqual([
            ['????#???? 1,2,1,1', 3880],
            ['????#???? 1,2,1', 3381560],
            ['????#???? 1,2', 366283],
            ['??? 1', 3003],
            ['??? 1,1', 1]],
            list_of_record_and_arrangement_count(self.partial_records, multiple=5))

    def test_should_find_arrangements_for_multiple_4(self):
        self.assertEqual([
            ['????#????.??? 1,2,1,1', 50316280],
            ['????#???? 1,2,1,1', 542],
            ['????#???? 1,2,1', 140574],
            ['????#???? 1,2', 22933],
            ['??? 1', 495],
            ['??? 1,1', 1]],
            list_of_record_and_arrangement_count(self.records, multiple=4))

    def test_should_find_arrangements(self):
        self.assertEqual([
            ['????#????.??? 1,2,1,1', 45],
            ['????#???? 1,2,1,1', 2],
            ['????#???? 1,2,1', 12],
            ['????#???? 1,2', 7],
            ['??? 1', 3],
            ['??? 1,1', 1]],
            list_of_record_and_arrangement_count(self.records))

    def test_should_find_arrangements_for_multiple_2(self):
        self.assertEqual([
            ['????#????.??? 1,2,1,1', 4414],
            ['????#???? 1,2,1,1', 11],
            ['????#???? 1,2,1', 256],
            ['????#???? 1,2', 97],
            ['??? 1', 15],
            ['??? 1,1', 1]],
            list_of_record_and_arrangement_count(self.records, multiple=2))

    def test_should_print_arrangements(self):
        verify(print_working_spring_arrangements_for_records(self.records))

    def test_should_print_arrangements_with_multiple_2(self):
        verify(print_working_spring_arrangements_for_records(self.records, multiple=2))

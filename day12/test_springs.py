import unittest

from approvaltests import verify

from day12.arrangements import total_spring_arrangements_from_file, total_spring_arrangements_from_records, \
    count_arrangements, generate_arrangements_list
from day12.springs import read_spring_conditions_from_file, read_spring_condition_line
from day12.springs_printer import print_working_spring_arrangements_for_file, list_of_record_and_arrangement_count, \
    print_working_spring_arrangements_for_records, print_record


class TestSprings(unittest.TestCase):

    def test_should_print_working_spring_arrangements_for_example(self):
        verify(print_working_spring_arrangements_for_file('example'))

    def test_should_count_arrangements_for_example_line_1(self):
        record = read_spring_condition_line("???.### 1,1,3")
        self.assertEqual(1, count_arrangements(record))

    def test_should_find_arrangements_for_example_line_3(self):
        record = read_spring_condition_line("?#?#?#?#?#?#?#? 1,3,1,6")
        self.assertEqual(['.#.###.#.######'], generate_arrangements_list(record))

    def test_should_find_arrangements_for_input_line_4(self):
        record = read_spring_condition_line("?#.#?#??#??? 1,7,1")
        self.assertEqual(['.#.#######.#'], generate_arrangements_list(record))

    def test_should_count_arrangements_for_input_line_9(self):
        record = read_spring_condition_line("?.#??.??#? 2,1,1")
        self.assertEqual(1, count_arrangements(record))

    def test_should_find_arrangements_for_input_line_11(self):
        record = read_spring_condition_line("?###?.??#??..? 5,4")
        self.assertEqual(['#####.####....', '#####..####...'], generate_arrangements_list(record))

    def test_should_print_working_spring_arrangements_for_input(self):
        verify(print_working_spring_arrangements_for_file('input'))

    def test_should_unfold_working_spring_arrangements_2_times_for_example(self):
        verify(print_working_spring_arrangements_for_file('example', multiple=2))

    def test_should_total_unfolded_working_spring_arrangements_for_example(self):
        records = read_spring_conditions_from_file('example')
        totals = list(map(lambda multiple: total_spring_arrangements_from_records(records, multiple),
                          [1, 2, 3, 4, 5]))
        self.assertEqual([21, 206, 2_612, 36_308, 525_152], totals)

    def test_should_unfold_working_spring_arrangements_5_times_for_example(self):
        self.assertEqual(525_152, total_spring_arrangements_from_file('example', multiple=5))

    def test_should_unfold_working_spring_arrangements_6_times_for_example(self):
        self.assertEqual(7_737_356, total_spring_arrangements_from_file('example', multiple=6))

    @unittest.skip('Too slow')
    def test_should_unfold_working_spring_arrangements_5_times_for_input(self):
        with open('output.log', 'w') as output:
            self.assertEqual(0, total_spring_arrangements_from_file('input', multiple=5, log=output))

    def test_should_unfold_arrangements_5_times_for_example_line_1(self):
        record = read_spring_condition_line("???.### 1,1,3")
        self.assertEqual(1, count_arrangements(record.unfold(5)))

    def test_should_unfold_arrangements_5_times_for_input_line_1(self):
        record = read_spring_condition_line("..???.??.? 1,1,1")
        self.assertEqual(5_752_544, count_arrangements(record.unfold(5)))

    def test_should_unfold_arrangements_5_times_for_input_line_24(self):
        record = read_spring_condition_line("??#?#?????????????. 8,4,1")
        self.assertEqual(67_192_396, count_arrangements(record.unfold(5)))

    @unittest.skip('Too slow')
    def test_should_unfold_arrangements_5_times_for_input_line_78(self):
        record = read_spring_condition_line("?????????.????????# 1,1,1,2,4")
        self.assertEqual(17_850_414_810_217, count_arrangements(record.unfold(5)))

    @unittest.skip('Too slow')
    def test_should_unfold_arrangements_5_times_for_input_line_167(self):
        record = read_spring_condition_line("?#?#?#?????????????? 6,1,1,1,1,1")
        self.assertEqual(0, count_arrangements(record.unfold(5)))


class TestSpringsInputLine41(unittest.TestCase):
    def setUp(self):
        self.records = [
            read_spring_condition_line("????#????.??? 1,2,1,1"),
            read_spring_condition_line("????#???? 1,2,1,1"),
            read_spring_condition_line("????#???? 1,2,1"),
            read_spring_condition_line("????#???? 1,2"),
            read_spring_condition_line("??? 1"),
            read_spring_condition_line("??? 1,1")
        ]
        self.partial_records = self.records[1:]
        self.record = self.records[0]

    def test_should_find_arrangements_unfolding_5_times(self):
        self.assertEqual(5486411504, count_arrangements(self.record.unfold(5)))

    def test_should_unfold_5_times(self):
        self.assertEqual('????#????.????????#????.????????#????.????????#????.????????#????.??? '
                         '1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1',
                         print_record(self.record.unfold(5)))

    def test_should_find_arrangements_for_partial_unfolding_5_times(self):
        self.assertEqual([
            ['????#???? 1,2,1,1', 3_880],
            ['????#???? 1,2,1', 3_381_560],
            ['????#???? 1,2', 366_283],
            ['??? 1', 3_003],
            ['??? 1,1', 1]],
            list_of_record_and_arrangement_count(self.partial_records, multiple=5))

    def test_should_find_arrangements_unfolding_4_times(self):
        self.assertEqual([
            ['????#????.??? 1,2,1,1', 50_316_280],
            ['????#???? 1,2,1,1', 542],
            ['????#???? 1,2,1', 140_574],
            ['????#???? 1,2', 22_933],
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

    def test_should_find_arrangements_unfolding_2_times(self):
        self.assertEqual([
            ['????#????.??? 1,2,1,1', 4_414],
            ['????#???? 1,2,1,1', 11],
            ['????#???? 1,2,1', 256],
            ['????#???? 1,2', 97],
            ['??? 1', 15],
            ['??? 1,1', 1]],
            list_of_record_and_arrangement_count(self.records, multiple=2))

    def test_should_print_arrangements(self):
        verify(print_working_spring_arrangements_for_records(self.records))

    def test_should_print_arrangements_unfolding_2_times(self):
        verify(print_working_spring_arrangements_for_records(self.records, multiple=2))

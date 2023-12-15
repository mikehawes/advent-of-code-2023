import unittest

from approvaltests import verify

from day15.hash import hash_string, sum_hashes_for_file, print_steps_for_file, get_total_focusing_power_for_file


class TestHash(unittest.TestCase):

    def test_should_hash_HASH(self):
        self.assertEqual(52, hash_string('HASH'))

    def test_should_sum_step_hashes_for_example(self):
        self.assertEqual(1320, sum_hashes_for_file('example'))

    def test_should_sum_step_hashes_for_input(self):
        self.assertEqual(505427, sum_hashes_for_file('input'))

    def test_should_print_steps_for_example(self):
        verify(print_steps_for_file('example'))

    def test_should_get_total_focusing_power_for_example(self):
        self.assertEqual(145, get_total_focusing_power_for_file('example'))

    def test_should_get_total_focusing_power_for_input(self):
        self.assertEqual(243747, get_total_focusing_power_for_file('input'))

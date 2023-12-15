import unittest

from day15.hash import hash_string, sum_hashes_for_file


class TestHash(unittest.TestCase):

    def test_should_hash_HASH(self):
        self.assertEqual(52, hash_string('HASH'))

    def test_should_sum_hashes_for_example(self):
        self.assertEqual(1320, sum_hashes_for_file('example'))

    def test_should_sum_hashes_for_input(self):
        self.assertEqual(505427, sum_hashes_for_file('input'))

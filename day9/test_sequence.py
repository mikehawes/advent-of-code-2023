import unittest

from approvaltests.approvals import verify

from day9.sequence import detect_sequences_from_file, sum_next_guesses_from_file
from day9.sequence_printer import print_sequences


class TestSequence(unittest.TestCase):

    def test_should_detect_sequences_for_example(self):
        verify(print_sequences(detect_sequences_from_file('example')))

    def test_should_sum_guesses_for_example(self):
        self.assertEqual(114, sum_next_guesses_from_file('example'))

    def test_should_detect_sequences_for_input(self):
        verify(print_sequences(detect_sequences_from_file('input')))

    def test_should_sum_guesses_for_input(self):
        self.assertEqual(1584748752, sum_next_guesses_from_file('input'))

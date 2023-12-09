import unittest

from approvaltests.approvals import verify

from day9.sequence import detect_sequences_from_file
from day9.sequence_printer import print_sequences


class TestSequence(unittest.TestCase):

    def test_should_detect_sequences_for_example(self):
        verify(print_sequences(detect_sequences_from_file('example')))

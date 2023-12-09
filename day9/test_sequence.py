import io
import unittest

from approvaltests.approvals import verify

from day9.sequence import detect_sequences_from_file


def print_sequences(sequences):
    output = io.StringIO()
    for sequence in sequences:
        number_strings = list(map(str, sequence.numbers))
        max_number_len = max(map(len, number_strings))
        print(' '.join(map(lambda s: s.rjust(max_number_len), number_strings)), file=output)
    return output.getvalue()


class TestSequence(unittest.TestCase):

    def test_should_detect_sequences_for_example(self):
        verify(print_sequences(detect_sequences_from_file('example')))

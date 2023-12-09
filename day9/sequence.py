import re


class SequenceDeltas:
    def __init__(self, numbers):
        self.numbers = numbers


def read_sequence_from_line(line):
    return list(map(int, re.findall("[0-9]+", line)))


def read_sequences_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_sequence_from_line, file))


def detect_sequences_from_file(input_file):
    sequences = read_sequences_from_file(input_file)
    return list(map(SequenceDeltas, sequences))

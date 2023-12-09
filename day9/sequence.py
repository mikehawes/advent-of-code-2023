import re


class SequenceDeltas:
    def __init__(self, numbers):
        self.numbers = numbers
        self.deltas = []
        max_delta = 1
        while max_delta > 0:
            deltas = []
            for i in range(0, len(numbers) - 1):
                a = numbers[i]
                b = numbers[i + 1]
                deltas.append(b - a)
            self.deltas.append(deltas)
            max_delta = max(deltas)
            numbers = deltas

    def guess_next_value(self):
        last_delta = 0
        next_delta = 0
        for deltas in self.deltas:
            next_delta = deltas[-1] + last_delta
            last_delta = next_delta
        return self.numbers[-1] + next_delta


def read_sequence_from_line(line):
    return list(map(int, re.findall("[0-9]+", line)))


def read_sequences_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_sequence_from_line, file))


def detect_sequences_from_file(input_file):
    sequences = read_sequences_from_file(input_file)
    return list(map(SequenceDeltas, sequences))

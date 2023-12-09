import re


class SequenceDeltas:
    def __init__(self, numbers):
        self.numbers = numbers
        self.deltas = []
        while any(filter(lambda d: d != 0, numbers)):
            deltas = []
            for i in range(0, len(numbers) - 1):
                a = numbers[i]
                b = numbers[i + 1]
                deltas.append(b - a)
            if len(deltas) == 0:
                raise 'Found empty deltas'
            else:
                self.deltas.append(deltas)
            numbers = deltas

    def guess_next_value(self):
        delta = 0
        for deltas in self.deltas:
            delta += deltas[-1]
        return self.numbers[-1] + delta


def read_sequence_from_line(line):
    return list(map(int, re.findall("-?[0-9]+", line)))


def read_sequences_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_sequence_from_line, file))


def detect_sequences_from_file(input_file):
    sequences = read_sequences_from_file(input_file)
    return list(map(SequenceDeltas, sequences))


def sum_next_guesses_from_file(input_file):
    sequences = detect_sequences_from_file(input_file)
    return sum(map(lambda s: s.guess_next_value(), sequences))

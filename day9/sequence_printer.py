import io


def number_strings(numbers):
    return map(str, numbers)


def join_strings(strings, width):
    return ' '.join(map(lambda s: s.rjust(width), strings))


def join_numbers(numbers, number_width):
    return join_strings(number_strings(numbers), number_width)


def print_sequences(sequences):
    output = io.StringIO()
    padding = 1
    for sequence in sequences:
        sequence_strings = list(number_strings(sequence.numbers))
        max_number_len = max(map(len, sequence_strings)) + padding
        print(join_strings(sequence_strings, max_number_len), file=output)
        indent = 1
        for deltas in sequence.deltas:
            print('{}{}'.format(
                ' ' * indent * int(max_number_len / 2 + padding),
                join_numbers(deltas, max_number_len)),
                file=output)
            indent += 1
        print(file=output)
    return output.getvalue()

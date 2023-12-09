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
    total_of_next_values = 0
    total_of_previous_values = 0
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
        next_value = sequence.guess_next_value()
        previous_value = sequence.guess_previous_value()
        total_of_next_values += next_value
        total_of_previous_values += previous_value
        print('Next value:', next_value, file=output)
        print('Previous value:', previous_value, file=output)
        print(file=output)

    print('Total of next values:', total_of_next_values, file=output)
    print('Total of previous values:', total_of_previous_values, file=output)
    return output.getvalue()

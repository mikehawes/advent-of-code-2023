def hash_string(string):
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value


def sum_hashes_for_file(input_file):
    with open(input_file, 'r') as file:
        steps = file.readline().strip().split(',')
    return sum(map(hash_string, steps))

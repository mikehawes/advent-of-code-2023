import re


def get_input():
    return open('input', 'r')


def is_symbol_adjacent_over_lines(match):
    span = match.span()
    if is_symbol_adjacent_on_line(symbols_by_line[line_index], span):
        return True
    if line_index > 0 and is_symbol_adjacent_on_line(symbols_by_line[line_index - 1], span):
        return True
    if line_index + 1 < len(symbols_by_line) and is_symbol_adjacent_on_line(symbols_by_line[line_index + 1], span):
        return True
    return False


def is_symbol_adjacent_on_line(symbol_indexes, span):
    for symbol_index in symbol_indexes:
        if span[0] - 1 <= symbol_index <= span[1]:
            return True
    return False


symbols_by_line = {}
line_index = 0
for line in get_input():
    line_symbols = []
    for symbol in re.finditer(r"[^0-9.\n]", line):
        line_symbols.append(symbol.start())
    symbols_by_line[line_index] = line_symbols
    line_index += 1

print(symbols_by_line)

part_numbers = []
line_index = 0
for line in get_input():
    for number in re.finditer(r"[0-9]+", line):
        if is_symbol_adjacent_over_lines(number):
            part_numbers.append(int(number.group(0)))
    line_index += 1

print(part_numbers)
print(sum(part_numbers))

import re


def read_and_expand_space_from_file(input_file):
    with open(input_file, 'r') as file:
        raw_lines = file.readlines()
    lines = []
    for i, raw_line in enumerate(raw_lines):
        line = raw_line.strip()
        if re.match(r'^\.+$', line):
            lines.append(line)
        lines.append(line)
    expanded_lines = lines.copy()
    col_expansions = 0
    for x in range(0, len(lines[0])):
        col_empty = True
        for y in range(0, len(lines)):
            if lines[y][x] != '.':
                col_empty = False
                break
        if col_empty:
            for y in range(0, len(expanded_lines)):
                line = expanded_lines[y]
                pos = x + col_expansions
                if pos < len(line) - 1:
                    expanded_lines[y] = line[:pos] + line[pos] + line[pos:]
                else:
                    expanded_lines[y] = line + line[pos]
            col_expansions += 1
    return expanded_lines

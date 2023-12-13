def load_patterns_from_file(input_file):
    with open(input_file, 'r') as file:
        pattern_lines = []
        patterns = []
        for raw_line in file:
            line = raw_line.strip()
            if len(line) == 0:
                patterns.append(pattern_lines)
                pattern_lines = []
            else:
                pattern_lines.append(list(line))
        patterns.append(pattern_lines)
        return patterns


class ReflectionLine:
    def __init__(self, is_horizontal, offset):
        self.is_horizontal = is_horizontal
        self.offset = offset


class ReflectionLines:
    def __init__(self, lines):
        self.lines = lines

    def score(self):
        total = 0
        for line in self.lines:
            if line.is_horizontal:
                total += line.offset + 1
            else:
                total += 100 * (line.offset + 1)
        return total


def find_reflection_lines(pattern_lines):
    height = len(pattern_lines)
    width = len(pattern_lines[0])
    x_values = []
    y_values = []
    for y in range(0, height - 1):
        is_reflection = True
        for i in range(0, min(y + 1, height - y - 1)):
            if pattern_lines[y - i] != pattern_lines[y + i + 1]:
                is_reflection = False
        if is_reflection:
            y_values.append(y)
    for x in range(0, width - 1):
        is_reflection = True
        for i in range(0, min(x + 1, width - x - 1)):
            for line in pattern_lines:
                if line[x - i] != line[x + i + 1]:
                    is_reflection = False
        if is_reflection:
            x_values.append(x)

    lines = []
    for value in x_values:
        lines.append(ReflectionLine(True, value))
    for value in y_values:
        lines.append(ReflectionLine(False, value))
    return ReflectionLines(lines)


def unsmudge_and_find_new_lines(pattern_lines, reflection_lines=None):
    height = len(pattern_lines)
    width = len(pattern_lines[0])
    unsmudged = pattern_lines.copy()
    if not reflection_lines:
        reflection_lines = find_reflection_lines(pattern_lines)
    line_smudged = reflection_lines.lines[0]
    for x in range(0, width):
        for y in range(0, height):
            line = unsmudged[y]
            old_char = line[x]
            if old_char == '.':
                line[x] = '#'
            else:
                line[x] = '.'
            found_unsmudged = find_reflection_lines(unsmudged)
            new_lines = []
            if found_unsmudged.lines:
                for found_line in found_unsmudged.lines:
                    if found_line.is_horizontal != line_smudged.is_horizontal or found_line.offset != line_smudged.offset:
                        new_lines.append(found_line)
            if new_lines:
                return unsmudged, ReflectionLines(new_lines)
            line[x] = old_char
    return pattern_lines, None


def print_pattern_lines(pattern_lines):
    for line in pattern_lines:
        print(''.join(line), flush=True)


def print_reflection_lines(reflections):
    for line in reflections.lines:
        if line.is_horizontal:
            print('Found reflection at x={}'.format(line.offset), flush=True)
        else:
            print('Found reflection at y={}'.format(line.offset), flush=True)


def compute_reflections_number_from_file(input_file):
    patterns = load_patterns_from_file(input_file)

    total = 0
    print()
    for pattern_lines in patterns:
        print_pattern_lines(pattern_lines)
        reflection_lines = find_reflection_lines(pattern_lines)
        print_reflection_lines(reflection_lines)
        total += reflection_lines.score()
        print()

    return total


def unsmudge_and_compute_reflections_number_from_file(input_file):
    patterns = load_patterns_from_file(input_file)

    total = 0
    print()
    for pattern_lines in patterns:
        print_pattern_lines(pattern_lines)
        reflection_lines = find_reflection_lines(pattern_lines)
        print_reflection_lines(reflection_lines)
        unsmudged, unsmudged_lines = unsmudge_and_find_new_lines(pattern_lines, reflection_lines)
        print_pattern_lines(unsmudged)
        print_reflection_lines(unsmudged_lines)
        total += unsmudged_lines.score()
        print()

    return total

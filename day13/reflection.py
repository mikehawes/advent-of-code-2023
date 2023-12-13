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
                pattern_lines.append(line)
        patterns.append(pattern_lines)
        return patterns


class ReflectionLines:
    def __init__(self, pattern_lines, x_values, y_values):
        self.pattern_lines = pattern_lines
        self.x_values = x_values
        self.y_values = y_values

    def score(self):
        total = 0
        for x in self.x_values:
            total += x + 1
        for y in self.y_values:
            total += 100 * (y + 1)
        return total


def find_reflection_lines(pattern_lines):
    height = len(pattern_lines)
    width = len(pattern_lines[0])
    x_values = []
    y_values = []
    for line in pattern_lines:
        print(line, flush=True)
    for y in range(0, height - 1):
        is_reflection = True
        for i in range(0, min(y + 1, height - y - 1)):
            if pattern_lines[y - i] != pattern_lines[y + i + 1]:
                is_reflection = False
        if is_reflection:
            y_values.append(y)
            print('Found reflection at y={}'.format(y), flush=True)
    for x in range(0, width - 1):
        is_reflection = True
        for i in range(0, min(x + 1, width - x - 1)):
            for line in pattern_lines:
                if line[x - i] != line[x + i + 1]:
                    is_reflection = False
        if is_reflection:
            x_values.append(x)
            print('Found reflection at x={}'.format(x), flush=True)
    return ReflectionLines(pattern_lines, x_values, y_values)


def compute_reflections_number_from_file(input_file):
    patterns = load_patterns_from_file(input_file)

    total = 0
    for pattern_lines in patterns:
        reflection_lines = find_reflection_lines(pattern_lines)
        total += reflection_lines.score()

    return total

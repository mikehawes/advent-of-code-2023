import re


class KnownDamagedArea:
    def __init__(self, match):
        self.match = match
        self.start = match.start()
        self.end = match.end()


class DamagedArea:
    def __init__(self, match):
        self.match = match
        self.start = match.start()
        self.end = match.end()
        self.length = self.end - self.start
        self.contents = match.group(0)
        self.known_damaged = list(map(KnownDamagedArea, re.finditer('#+', self.contents)))


class SpringConditionRecord:
    def __init__(self, springs, damaged_counts):
        self.springs = springs
        self.damaged_counts = damaged_counts
        self.damaged_areas = list(map(DamagedArea, re.finditer(r'[?#]+', springs)))


def read_spring_condition_line(line):
    parts = line.rstrip().split(' ')
    return SpringConditionRecord(parts[0], list(map(int, parts[1].split(','))))


def read_spring_conditions_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_spring_condition_line, file))

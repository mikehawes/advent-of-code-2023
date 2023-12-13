import itertools
import re


class Area:
    def __init__(self, contents):
        self.length = len(contents)
        self.contents = contents
        self.type = self.contents[0]
        self.known = self.type != '?'
        self.damaged = self.type == '#'


def area_from_match(match):
    return Area(match.group(0))


class DamagedArea:
    def __init__(self, match):
        self.match = match
        self.start = match.start()
        self.end = match.end()
        self.length = self.end - self.start
        self.contents = match.group(0)
        self.areas = list(map(area_from_match, re.finditer(r'#+|\?+', self.contents)))
        self.known_damaged = list(filter(lambda a: a.known, self.areas))
        self.unknown_areas = list(filter(lambda a: not a.known, self.areas))
        self.fully_known = len(self.known_damaged) == 1 and self.length == self.known_damaged[0].length
        self.fully_unknown = len(self.unknown_areas) == 1 and self.length == self.unknown_areas[0].length


class SpringConditionRecord:
    def __init__(self, springs, damaged_counts, unfolded_from=None):
        self.springs = springs
        self.damaged_counts = damaged_counts
        self.unfolded_from = unfolded_from
        self.areas = list(map(area_from_match, re.finditer(r'#+|\.+|\?+', springs)))
        self.damaged_areas = list(map(DamagedArea, re.finditer(r'[?#]+', springs)))

    def unfold(self, multiple):
        if multiple == 1:
            return self
        springs = '?'.join(itertools.repeat(self.springs, multiple))
        damaged_counts = self.damaged_counts * multiple
        return SpringConditionRecord(springs, damaged_counts, unfolded_from=self)


def read_spring_condition_line(line):
    parts = line.rstrip().split(' ')
    return SpringConditionRecord(parts[0], list(map(int, parts[1].split(','))))


def read_spring_conditions_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_spring_condition_line, file))

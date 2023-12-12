import re


class Area:
    def __init__(self, match):
        self.match = match
        self.start = match.start()
        self.end = match.end()
        self.length = self.end - self.start
        self.contents = match.group(0)
        self.type = self.contents[0]
        self.known = self.type != '?'


def generate_all_fillings(areas, area_index=0, area_offset=0, filling_start=''):
    if area_index >= len(areas):
        return [filling_start]
    area = areas[area_index]
    if area.known:
        return generate_all_fillings(areas, area_index + 1, 0, filling_start + area.contents)
    if area_offset >= area.length:
        return generate_all_fillings(areas, area_index + 1, 0, filling_start)
    fillings_with_damaged = generate_all_fillings(areas, area_index, area_offset + 1, filling_start + '#')
    fillings_with_undamaged = generate_all_fillings(areas, area_index, area_offset + 1, filling_start + '.')
    return fillings_with_damaged + fillings_with_undamaged


def find_damaged_counts(springs):
    counts = []
    num_damaged = 0
    for spring in springs:
        if spring == '#':
            num_damaged += 1
        elif num_damaged > 0:
            counts.append(num_damaged)
            num_damaged = 0
    if num_damaged > 0:
        counts.append(num_damaged)
    return counts


class DamagedArea:
    def __init__(self, match):
        self.match = match
        self.start = match.start()
        self.end = match.end()
        self.length = self.end - self.start
        self.contents = match.group(0)
        self.areas = list(map(Area, re.finditer(r'#+|\?+', self.contents)))
        self.known_damaged = list(filter(lambda a: a.known, self.areas))
        self.unknown_areas = list(filter(lambda a: not a.known, self.areas))
        self.fully_known = len(self.known_damaged) == 1 and self.length == self.known_damaged[0].length
        self.fully_unknown = len(self.unknown_areas) == 1 and self.length == self.unknown_areas[0].length

    def generate_all_fillings(self):
        return generate_all_fillings(self.areas)


class SpringArrangements:
    def __init__(self, record, fillings, arrangements):
        self.record = record
        self.fillings = fillings
        self.arrangements = arrangements


class SpringConditionRecord:
    def __init__(self, springs, damaged_counts):
        self.springs = springs
        self.damaged_counts = damaged_counts
        self.areas = list(map(Area, re.finditer(r'#+|\.+|\?+', springs)))
        self.damaged_areas = list(map(DamagedArea, re.finditer(r'[?#]+', springs)))

    def generate_all_fillings(self):
        return generate_all_fillings(self.areas)

    def possible_fillings(self, fillings=None):
        if not fillings:
            fillings = self.generate_all_fillings()
        possible = []
        for filling in fillings:
            damaged_counts = find_damaged_counts(filling)
            if damaged_counts == self.damaged_counts:
                possible.append(filling)
        return possible

    def arrangements(self):
        fillings = self.generate_all_fillings()
        arrangements = self.possible_fillings(fillings)
        return SpringArrangements(self, fillings, arrangements)


def read_spring_condition_line(line):
    parts = line.rstrip().split(' ')
    return SpringConditionRecord(parts[0], list(map(int, parts[1].split(','))))


def read_spring_conditions_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_spring_condition_line, file))

import re
from math import prod


class Area:
    def __init__(self, match):
        self.match = match
        self.start = match.start()
        self.end = match.end()
        self.length = self.end - self.start
        self.contents = match.group(0)
        self.type = self.contents[0]
        self.known = self.type != '?'
        self.damaged = self.type == '#'


def generate_arrangements(areas, damaged_counts, remaining_unknown, remaining_unknown_damaged,
                          damaged_count=0, force_undamaged=False,
                          area_index=0, area_offset=0, filling_start=''):
    if remaining_unknown < remaining_unknown_damaged:
        return []
    if len(damaged_counts) == 0:
        force_undamaged = True
    elif damaged_count > damaged_counts[0]:
        return []
    elif damaged_count == damaged_counts[0]:
        damaged_counts = damaged_counts[1:]
        damaged_count = 0
        force_undamaged = True
    if area_index >= len(areas):
        if len(damaged_counts) > 0:
            return []
        else:
            return [filling_start]
    area = areas[area_index]
    if area.known:
        if force_undamaged and area.damaged:
            return []
        if damaged_count > 0 and not area.damaged:
            return []
        found_damaged = area.length if area.damaged else 0
        return generate_arrangements(areas, damaged_counts, remaining_unknown, remaining_unknown_damaged,
                                     damaged_count + found_damaged, False,
                                     area_index + 1, 0, filling_start + area.contents)
    if area_offset >= area.length:
        return generate_arrangements(areas, damaged_counts, remaining_unknown, remaining_unknown_damaged,
                                     damaged_count, force_undamaged,
                                     area_index + 1, 0, filling_start)
    arrangements = []
    if damaged_count == 0:
        arrangements += generate_arrangements(areas, damaged_counts, remaining_unknown - 1, remaining_unknown_damaged,
                                              0, False,
                                              area_index, area_offset + 1, filling_start + '.')
    if not force_undamaged:
        arrangements += generate_arrangements(areas, damaged_counts, remaining_unknown - 1,
                                              remaining_unknown_damaged - 1,
                                              damaged_count + 1, force_undamaged,
                                              area_index, area_offset + 1, filling_start + '#')
    return arrangements


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


class SpringArrangements:
    def __init__(self, record, fillings_count, arrangements):
        self.record = record
        self.fillings_count = fillings_count
        self.arrangements = arrangements
        self.arrangements_count = len(arrangements)


class SpringConditionRecord:
    def __init__(self, springs, damaged_counts):
        self.springs = springs
        self.damaged_counts = damaged_counts
        self.areas = list(map(Area, re.finditer(r'#+|\.+|\?+', springs)))
        self.damaged_areas = list(map(DamagedArea, re.finditer(r'[?#]+', springs)))

    def arrangements(self):
        fillings_count = prod(map(lambda a: 1 if a.known else 2 ** a.length, self.areas))
        unknown = sum(map(lambda a: a.length, filter(lambda a: not a.known, self.areas)))
        known_damaged = sum(map(lambda a: a.length, filter(lambda a: a.damaged, self.areas)))
        unknown_damaged = sum(self.damaged_counts) - known_damaged
        arrangements = generate_arrangements(self.areas, self.damaged_counts, unknown, unknown_damaged)
        return SpringArrangements(self, fillings_count, arrangements)


def read_spring_condition_line(line):
    parts = line.rstrip().split(' ')
    return SpringConditionRecord(parts[0], list(map(int, parts[1].split(','))))


def read_spring_conditions_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_spring_condition_line, file))

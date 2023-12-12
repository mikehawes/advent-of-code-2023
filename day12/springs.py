import re


class Area:
    def __init__(self, match):
        self.match = match
        self.start = match.start()
        self.end = match.end()
        self.length = self.end - self.start
        self.contents = match.group(0)
        self.known = self.contents.startswith('#')


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

    def generate_all_fillings(self, area_index=0, area_offset=0, filling_start=''):
        if area_index >= len(self.areas):
            return [filling_start]
        area = self.areas[area_index]
        if area.known:
            return self.generate_all_fillings(area_index + 1, 0, filling_start + area.contents)
        if area_offset >= area.length:
            return self.generate_all_fillings(area_index + 1, 0, filling_start)
        fillings_with_damaged = self.generate_all_fillings(area_index, area_offset + 1, filling_start + '#')
        fillings_with_undamaged = self.generate_all_fillings(area_index, area_offset + 1, filling_start + '.')
        return fillings_with_damaged + fillings_with_undamaged


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

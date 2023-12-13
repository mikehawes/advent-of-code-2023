import datetime
import itertools
import re
import time

from day12.arrangements import generate_arrangements


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

    def arrangements(self, count_only=False):
        return generate_arrangements(self, count_only)

    def count_arrangements(self, multiple=1):
        return self.unfold(multiple).arrangements(count_only=True).arrangements_count

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


def compute_spring_arrangements_from_file(input_file, multiple=1, count_only=False):
    records = read_spring_conditions_from_file(input_file)
    return compute_spring_arrangements_from_records(records, multiple, count_only)


def compute_spring_arrangements_from_records(records, multiple=1, count_only=False):
    arrangements = []
    num_records = len(records)
    start = time.time()
    print('Computing arrangements for {} records'.format(num_records))
    for i, record in enumerate(records):
        record_arrangements = record.unfold(multiple).arrangements(count_only=count_only)
        arrangements.append(record_arrangements)
        print("Computed {} of {} records, count {}, time so far: {}"
              .format(i + 1, num_records, record_arrangements.arrangements_count,
                      datetime.timedelta(seconds=time.time() - start)))
    return arrangements


def total_spring_arrangements(arrangements):
    return sum(map(lambda a: a.arrangements_count, arrangements))


def total_spring_arrangements_from_file(input_file, multiple=1):
    record_arrangements = compute_spring_arrangements_from_file(input_file, multiple=multiple, count_only=True)
    return total_spring_arrangements(record_arrangements)


def total_spring_arrangements_from_records(records, multiple=1):
    record_arrangements = compute_spring_arrangements_from_records(records, multiple=multiple, count_only=True)
    return total_spring_arrangements(record_arrangements)

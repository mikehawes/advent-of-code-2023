import datetime
import re
import time
from math import prod


class Area:
    def __init__(self, contents):
        self.length = len(contents)
        self.contents = contents
        self.type = self.contents[0]
        self.known = self.type != '?'
        self.damaged = self.type == '#'


def area_from_match(match):
    return Area(match.group(0))


class FindArrangementsState:
    def __init__(self, damaged_counts=None, remaining_unknown=None, remaining_unknown_damaged=None,
                 damaged_count=0, force_undamaged=False, area_index=0, area_offset=0, valid=True):
        if not valid:
            self.valid = False
            return
        self.damaged_counts = damaged_counts
        self.remaining_unknown = remaining_unknown
        self.remaining_unknown_damaged = remaining_unknown_damaged
        self.damaged_count = damaged_count
        self.force_undamaged = force_undamaged
        self.area_index = area_index
        self.area_offset = area_offset
        self.valid = True
        if remaining_unknown < remaining_unknown_damaged:
            self.valid = False
        elif len(damaged_counts) == 0:
            self.force_undamaged = True
        elif damaged_count > damaged_counts[0]:
            self.valid = False
        elif damaged_count == damaged_counts[0]:
            self.damaged_counts = damaged_counts[1:]
            self.damaged_count = 0
            self.force_undamaged = True

    def after_known_area(self, area):
        if self.force_undamaged and area.damaged:
            return FindArrangementsState(valid=False)
        if self.damaged_count > 0 and not area.damaged:
            return FindArrangementsState(valid=False)
        found_damaged = area.length if area.damaged else 0
        return FindArrangementsState(self.damaged_counts, self.remaining_unknown, self.remaining_unknown_damaged,
                                     self.damaged_count + found_damaged, False, self.area_index + 1, 0)

    def next_area(self):
        return FindArrangementsState(self.damaged_counts, self.remaining_unknown, self.remaining_unknown_damaged,
                                     self.damaged_count, self.force_undamaged, self.area_index + 1, 0)

    def chose_unknown_undamaged(self):
        return FindArrangementsState(self.damaged_counts, self.remaining_unknown - 1, self.remaining_unknown_damaged,
                                     0, False, self.area_index, self.area_offset + 1)

    def chose_unknown_damaged(self):
        return FindArrangementsState(self.damaged_counts, self.remaining_unknown - 1,
                                     self.remaining_unknown_damaged - 1,
                                     self.damaged_count + 1, False, self.area_index, self.area_offset + 1)


def generate_arrangements(areas, state, count_only, filling_start=''):
    state_stack = []
    filling_stack = []
    arrangements = 0 if count_only else []
    while True:
        if not state.valid:
            if state_stack:
                state = state_stack.pop()
                filling_start = filling_stack.pop()
            else:
                return arrangements
            continue
        if state.area_index >= len(areas):
            if len(state.damaged_counts) == 0:
                if count_only:
                    arrangements += 1
                else:
                    arrangements.append(filling_start)
            if state_stack:
                state = state_stack.pop()
                filling_start = filling_stack.pop()
            else:
                return arrangements
            continue
        area = areas[state.area_index]
        if area.known:
            state = state.after_known_area(area)
            filling_start += area.contents
            continue
        if state.area_offset >= area.length:
            state = state.next_area()
            continue
        if state.damaged_count == 0:
            state_stack.append(state.chose_unknown_undamaged())
            filling_stack.append(filling_start + '.')
        if not state.force_undamaged:
            state_stack.append(state.chose_unknown_damaged())
            filling_stack.append(filling_start + '#')
        state = state_stack.pop()
        filling_start = filling_stack.pop()


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


class SpringArrangements:
    def __init__(self, record, fillings_count, arrangements):
        self.record = record
        self.fillings_count = fillings_count
        if isinstance(arrangements, list):
            self.arrangements = arrangements
            self.arrangements_count = len(arrangements)
        else:
            self.arrangements_count = arrangements


class SpringConditionRecord:
    def __init__(self, springs, damaged_counts):
        self.springs = springs
        self.damaged_counts = damaged_counts
        self.areas = list(map(area_from_match, re.finditer(r'#+|\.+|\?+', springs)))
        self.damaged_areas = list(map(DamagedArea, re.finditer(r'[?#]+', springs)))

    def arrangements(self, multiple=1, count_only=False):
        areas = []
        for i in range(0, multiple):
            if i != 0:
                areas.append(Area('?'))
            areas.extend(self.areas)
        damaged_counts = self.damaged_counts * multiple
        fillings_count = prod(map(lambda a: 1 if a.known else 2 ** a.length, areas))
        unknown = sum(map(lambda a: a.length, filter(lambda a: not a.known, areas)))
        known_damaged = sum(map(lambda a: a.length, filter(lambda a: a.damaged, areas)))
        unknown_damaged = sum(damaged_counts) - known_damaged
        arrangements = generate_arrangements(areas, FindArrangementsState(damaged_counts, unknown, unknown_damaged),
                                             count_only)
        return SpringArrangements(self, fillings_count, arrangements)

    def count_arrangements(self, multiple=1):
        return self.arrangements(multiple=multiple, count_only=True).arrangements_count


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
        record_arrangements = record.arrangements(multiple=multiple, count_only=count_only)
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

import datetime
import math
import time

from day12.springs import read_spring_conditions_from_file, SpringConditionRecord


class SpringArrangements:
    def __init__(self, record, arrangements):
        self.record = record
        self.fillings_count = math.prod(map(lambda a: 1 if a.known else 2 ** a.length, record.areas))
        if isinstance(arrangements, list):
            self.arrangements = arrangements
            self.arrangements_count = len(arrangements)
        else:
            self.arrangements_count = arrangements


class FindArrangementsState:
    def __init__(self, damaged_counts=None, remaining_unknown=None, remaining_unknown_damaged=None,
                 damaged_count=0, force_undamaged=False, area_index=0, area_offset=0, valid=True):
        if not valid or remaining_unknown < remaining_unknown_damaged:
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
        if not damaged_counts:
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


def generate_arrangements(record, count_only):
    arrangements = __generate_arrangements(record, count_only)
    return SpringArrangements(record, arrangements)


def count_arrangements(record):
    return __generate_arrangements(record, count_only=True)


def compute_spring_arrangements_from_file(input_file, multiple=1, count_only=False):
    records = read_spring_conditions_from_file(input_file)
    return compute_spring_arrangements_from_records(records, multiple, count_only)


def compute_spring_arrangements_from_records(records, multiple=1, count_only=False):
    arrangements = []
    num_records = len(records)
    start = time.time()
    print('Computing arrangements for {} records'.format(num_records))
    for i, record in enumerate(records):
        record_arrangements = generate_arrangements(record.unfold(multiple), count_only=count_only)
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


def __generate_arrangments_index(record, count_only):
    length = len(record.springs)
    index_start = int(length / 2)
    index_springs = record.springs[index_start:]
    arrangements_by_remaining_counts = {}
    for i in range(0, len(record.damaged_counts)):
        remaining_counts = record.damaged_counts[i:]
        remaining_counts_str = ','.join(map(str, remaining_counts))
        index_record = SpringConditionRecord(index_springs, remaining_counts)
        index_arrangements = generate_arrangements(index_record, count_only)
        if index_arrangements.arrangements_count > 0:
            arrangements_by_remaining_counts[remaining_counts_str] = index_arrangements


def __initial_state(record):
    unknown = sum(map(lambda a: a.length, filter(lambda a: not a.known, record.areas)))
    known_damaged = sum(map(lambda a: a.length, filter(lambda a: a.damaged, record.areas)))
    unknown_damaged = sum(record.damaged_counts) - known_damaged
    return FindArrangementsState(record.damaged_counts, unknown, unknown_damaged)


def __generate_arrangements(record, count_only):
    state = __initial_state(record)
    areas = record.areas
    state_stack = []
    filling_stack = []
    filling_start = ''
    arrangements = 0 if count_only else []
    while True:
        if not state.valid:
            if state_stack:
                state = state_stack.pop()
                if not count_only:
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
                if not count_only:
                    filling_start = filling_stack.pop()
            else:
                return arrangements
            continue
        area = areas[state.area_index]
        if area.known:
            state = state.after_known_area(area)
            if not count_only:
                filling_start += area.contents
            continue
        if state.area_offset >= area.length:
            state = state.next_area()
            continue
        if state.damaged_count == 0:
            state_stack.append(state.chose_unknown_undamaged())
            if not count_only:
                filling_stack.append(filling_start + '.')
        if not state.force_undamaged:
            state_stack.append(state.chose_unknown_damaged())
            if not count_only:
                filling_stack.append(filling_start + '#')
        state = state_stack.pop()
        if not count_only:
            filling_start = filling_stack.pop()

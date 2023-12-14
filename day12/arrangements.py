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


def generate_arrangements(record, count_only=False):
    arrangements = __generate_arrangements(record, count_only)
    return SpringArrangements(record, arrangements)


def generate_arrangements_list(record):
    return __generate_arrangements(record, count_only=False)


def count_arrangements(record):
    return __generate_arrangements(record, count_only=True)


def compute_spring_arrangements_from_records(records, multiple=1, count_only=False, log=None):
    arrangements = []
    num_records = len(records)
    start = time.time()
    print('Computing arrangements for {} records'.format(num_records), file=log, flush=True)
    for i, record in enumerate(records):
        record_arrangements = generate_arrangements(record.unfold(multiple), count_only=count_only)
        arrangements.append(record_arrangements)
        print("Computed {} of {} records, count {}, time so far: {}"
              .format(i + 1, num_records, record_arrangements.arrangements_count,
                      datetime.timedelta(seconds=time.time() - start)), file=log, flush=True)
    return arrangements


def total_spring_arrangements(arrangements):
    return sum(map(lambda a: a.arrangements_count, arrangements))


def total_spring_arrangements_from_file(input_file, multiple=1, log=None):
    records = read_spring_conditions_from_file(input_file)
    record_arrangements = compute_spring_arrangements_from_records(
        records, multiple=multiple, count_only=True, log=log)
    return total_spring_arrangements(record_arrangements)


def total_spring_arrangements_from_records(records, multiple=1):
    record_arrangements = compute_spring_arrangements_from_records(records, multiple=multiple, count_only=True)
    return total_spring_arrangements(record_arrangements)


class SpringArrangementsIndex:
    def __init__(self, area_index, area_offset, arrangements_by_remaining_counts):
        self.area_index = area_index
        self.area_offset = area_offset
        self.arrangements_by_remaining_counts = arrangements_by_remaining_counts

    def remaining_arrangements_for_state(self, state):
        damaged_counts = state.damaged_counts.copy()
        damaged_counts[0] -= state.damaged_count
        remaining_counts_str = ','.join(map(str, damaged_counts))
        if remaining_counts_str not in self.arrangements_by_remaining_counts:
            return []
        arrangements = self.arrangements_by_remaining_counts[remaining_counts_str]
        if state.force_undamaged:
            return list(filter(lambda a: a.startswith('.'), arrangements))
        else:
            return arrangements


def __generate_arrangments_index(record):
    half_length = int(len(record.springs) / 2)
    pos = 0
    index_start = len(record.springs)
    area_index = len(record.areas)
    area_offset = 0
    for i, area in enumerate(record.areas):
        if not area.known and pos > half_length:
            area_index = i
            index_start = pos
            area_offset = 0
            break
        pos += area.length
    arrangements_by_remaining_counts = {}
    if index_start == len(record.springs):
        return SpringArrangementsIndex(area_index, area_offset, arrangements_by_remaining_counts)
    index_springs = record.springs[index_start:]
    remaining_counts = record.damaged_counts.copy()
    refuse_undamaged_start = False
    while remaining_counts:
        index_record = SpringConditionRecord(index_springs, remaining_counts)
        index_arrangements = __generate_arrangements(index_record, False, generate_index=False)
        if refuse_undamaged_start:
            index_arrangements = list(filter(lambda a: a.startswith('#'), index_arrangements))
        if index_arrangements:
            remaining_counts_str = ','.join(map(str, remaining_counts))
            arrangements_by_remaining_counts[remaining_counts_str] = index_arrangements
        remaining_counts[0] -= 1
        refuse_undamaged_start = True
        if remaining_counts[0] == 0:
            remaining_counts = remaining_counts[1:]
            refuse_undamaged_start = False
    return SpringArrangementsIndex(area_index, area_offset, arrangements_by_remaining_counts)


def __initial_state(record):
    unknown = sum(map(lambda a: a.length, filter(lambda a: not a.known, record.areas)))
    known_damaged = sum(map(lambda a: a.length, filter(lambda a: a.damaged, record.areas)))
    unknown_damaged = sum(record.damaged_counts) - known_damaged
    return FindArrangementsState(record.damaged_counts, unknown, unknown_damaged)


def __generate_arrangements(record, count_only, generate_index=True):
    state = __initial_state(record)
    if generate_index:
        index = __generate_arrangments_index(record)
    else:
        index = None
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
        terminated = False
        if (index and state.damaged_counts
                and state.area_index == index.area_index
                and state.area_offset == index.area_offset):
            terminated = True
            remaining = index.remaining_arrangements_for_state(state)
            if count_only:
                arrangements += len(remaining)
            else:
                for arrangement in remaining:
                    arrangements.append(filling_start + arrangement)
        elif state.area_index >= len(areas):
            terminated = True
            if len(state.damaged_counts) == 0:
                if count_only:
                    arrangements += 1
                else:
                    arrangements.append(filling_start)
        if terminated:
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

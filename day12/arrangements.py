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


def generate_arrangements(record, count_only=False, log=None):
    arrangements = __generate_arrangements(record, count_only, log)
    return SpringArrangements(record, arrangements)


def generate_arrangements_list(record, log=None):
    return __generate_arrangements(record, count_only=False, log=log)


def count_arrangements(record, log=None):
    return __generate_arrangements(record, count_only=True, log=log)


def compute_spring_arrangements_from_records(records, multiple=1, count_only=False, log=None):
    arrangements = []
    num_records = len(records)
    start = time.time()
    print('Computing arrangements for {} records'.format(num_records), file=log, flush=True)
    for i, record in enumerate(records):
        unfolded = record.unfold(multiple)
        print('Computing arrangements for springs: ', unfolded.springs)
        record_arrangements = generate_arrangements(unfolded, count_only=count_only, log=log)
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


class SpringArrangementsIndex:
    def __init__(self, index_start, area_index, area_offset,
                 arrangements_by_remaining_counts, undamaged_arrangements_by_remaining_counts=None):
        self.index_start = index_start
        self.area_index = area_index
        self.area_offset = area_offset
        self.empty = not arrangements_by_remaining_counts
        self.arrangements_by_remaining_counts = arrangements_by_remaining_counts
        if undamaged_arrangements_by_remaining_counts:
            self.undamaged_arrangements_by_remaining_counts = undamaged_arrangements_by_remaining_counts
        else:
            self.undamaged_arrangements_by_remaining_counts = {}
            for counts, arrangements in arrangements_by_remaining_counts.items():
                undamaged = list(filter(lambda a: a.startswith('.'), arrangements))
                if undamaged:
                    self.undamaged_arrangements_by_remaining_counts[counts] = undamaged

    def remaining_arrangements_for_state(self, state):
        damaged_counts = state.damaged_counts.copy()
        damaged_counts[0] -= state.damaged_count
        remaining_counts_str = ','.join(map(str, damaged_counts))
        if state.force_undamaged:
            if remaining_counts_str not in self.undamaged_arrangements_by_remaining_counts:
                return []
            return self.undamaged_arrangements_by_remaining_counts[remaining_counts_str]
        else:
            if remaining_counts_str not in self.arrangements_by_remaining_counts:
                return []
            return self.arrangements_by_remaining_counts[remaining_counts_str]

    def minus_offsets(self, start, area_index, area_offset):
        return SpringArrangementsIndex(
            self.index_start - start, self.area_index - area_index, self.area_offset - area_offset,
            self.arrangements_by_remaining_counts, self.undamaged_arrangements_by_remaining_counts)


def __generate_arrangments_index(record, indexes_so_far, prev_index, log=None):
    target_pos = int(record.num_springs / (2 ** (indexes_so_far + 1)))
    pos = 0
    index_start = record.num_springs
    area_index = record.num_areas
    area_offset = 0
    for i, area in enumerate(record.areas):
        if prev_index and i == prev_index.area_index:
            return prev_index
        area_end = pos + area.length
        if not area.known:
            if pos > target_pos:
                area_index = i
                index_start = pos
                area_offset = 0
                break
            elif area_end > target_pos:
                area_index = i
                index_start = target_pos
                area_offset = target_pos - pos
                break
        pos += area.length
    print('Index start:', index_start, file=log)
    print('Area index:', area_index, file=log)
    print('Area offset:', area_offset, file=log)
    arrangements_by_remaining_counts = {}
    if index_start == record.num_springs:
        return SpringArrangementsIndex(index_start, area_index, area_offset, arrangements_by_remaining_counts)

    area = record.areas[area_index]
    print('Area:', area.contents, file=log)
    before_index = max(0, area.start_index - 2)
    after_index = min(record.num_springs, area.start_index + area.length + 2)
    print('Around area:', record.springs[before_index:after_index], file=log)
    index_springs = record.springs[index_start:]
    print('Index springs:', index_springs, file=log)
    remaining_counts = record.damaged_counts.copy()
    if prev_index:
        minus_area_offset = area_offset if area_index == prev_index.area_index else 0
        prev_index = prev_index.minus_offsets(index_start, area_index, minus_area_offset)
    refuse_undamaged_start = False
    while remaining_counts:
        index_record = SpringConditionRecord(index_springs, remaining_counts)
        index_arrangements = __generate_arrangements(
            index_record, count_only=False, generate_indexes=0, index=prev_index)
        if index_arrangements:
            if refuse_undamaged_start:
                index_arrangements = list(filter(lambda a: a.startswith('#'), index_arrangements))
            remaining_counts_str = ','.join(map(str, remaining_counts))
            arrangements_by_remaining_counts[remaining_counts_str] = index_arrangements
        remaining_counts[0] -= 1
        if remaining_counts[0] == 0:
            remaining_counts = remaining_counts[1:]
            refuse_undamaged_start = False
        else:
            refuse_undamaged_start = True
    return SpringArrangementsIndex(index_start, area_index, area_offset, arrangements_by_remaining_counts)


def __initial_state(record):
    unknown = sum(map(lambda a: a.length, filter(lambda a: not a.known, record.areas)))
    known_damaged = sum(map(lambda a: a.length, filter(lambda a: a.damaged, record.areas)))
    unknown_damaged = sum(record.damaged_counts) - known_damaged
    return FindArrangementsState(record.damaged_counts, unknown, unknown_damaged)


def __generate_arrangements(record, count_only, log=None, generate_indexes=2, index=None):
    state = __initial_state(record)
    for i in range(0, generate_indexes):
        start = time.time()
        print('Generating index', i, file=log)
        print('Record length:', record.num_springs, file=log)
        index = __generate_arrangments_index(record, i, index, log=log)
        end = time.time()
        print('Generated index', i, 'in', datetime.timedelta(seconds=end - start), file=log)
        print('Indexed remaining counts:', len(index.arrangements_by_remaining_counts), flush=True, file=log)
    areas = record.areas
    state_stack = []
    filling_stack = []
    filling_start = ''
    arrangements = 0 if count_only else []
    while True:
        terminated = False
        if not state.valid:
            terminated = True
        elif (index and state.damaged_counts
              and state.area_index == index.area_index
              and state.area_offset == index.area_offset):
            terminated = True
            remaining = index.remaining_arrangements_for_state(state)
            if count_only:
                arrangements += len(remaining)
            else:
                for arrangement in remaining:
                    arrangements.append(filling_start + arrangement)
        elif state.area_index >= record.num_areas:
            terminated = True
            if not state.damaged_counts:
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

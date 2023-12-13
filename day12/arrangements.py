import math


class SpringArrangements:
    def __init__(self, record, fillings_count, arrangements):
        self.record = record
        self.fillings_count = fillings_count
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
    fillings_count = math.prod(map(lambda a: 1 if a.known else 2 ** a.length, record.areas))
    unknown = sum(map(lambda a: a.length, filter(lambda a: not a.known, record.areas)))
    known_damaged = sum(map(lambda a: a.length, filter(lambda a: a.damaged, record.areas)))
    unknown_damaged = sum(record.damaged_counts) - known_damaged
    state = FindArrangementsState(record.damaged_counts, unknown, unknown_damaged)
    arrangements = __generate_arrangements_with_state(record.areas, state, count_only)
    return SpringArrangements(record, fillings_count, arrangements)


def __generate_arrangements_with_state(areas, state, count_only):
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

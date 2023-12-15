import io
from copy import deepcopy


class PlatformState:
    def __init__(self, lines):
        self.lines = lines
        self.height = len(self.lines)
        self.width = len(self.lines[0])

    def tilt_north(self):
        new_lines = deepcopy(self.lines)
        for y in range(0, self.height):
            for x in range(0, self.width):
                if new_lines[y][x] == '.':
                    for y2 in range(y + 1, self.height):
                        tile2 = new_lines[y2][x]
                        if tile2 == 'O':
                            new_lines[y][x] = 'O'
                            new_lines[y2][x] = '.'
                            break
                        elif tile2 == '#':
                            break
        return PlatformState(new_lines)

    def tilt_west(self):
        new_lines = deepcopy(self.lines)
        for x in range(0, self.width):
            for y in range(0, self.height):
                if new_lines[y][x] == '.':
                    for x2 in range(x + 1, self.width):
                        tile2 = new_lines[y][x2]
                        if tile2 == 'O':
                            new_lines[y][x] = 'O'
                            new_lines[y][x2] = '.'
                            break
                        elif tile2 == '#':
                            break
        return PlatformState(new_lines)

    def tilt_east(self):
        new_lines = deepcopy(self.lines)
        for x in range(self.width - 1, -1, -1):
            for y in range(0, self.height):
                if new_lines[y][x] == '.':
                    for x2 in range(x - 1, -1, -1):
                        tile2 = new_lines[y][x2]
                        if tile2 == 'O':
                            new_lines[y][x] = 'O'
                            new_lines[y][x2] = '.'
                            break
                        elif tile2 == '#':
                            break
        return PlatformState(new_lines)

    def tilt_south(self):
        new_lines = deepcopy(self.lines)
        for y in range(self.height - 1, -1, -1):
            for x in range(0, self.width):
                if new_lines[y][x] == '.':
                    for y2 in range(y - 1, -1, -1):
                        tile2 = new_lines[y2][x]
                        if tile2 == 'O':
                            new_lines[y][x] = 'O'
                            new_lines[y2][x] = '.'
                            break
                        elif tile2 == '#':
                            break
        return PlatformState(new_lines)

    def spin_cycle(self):
        return self.tilt_north().tilt_west().tilt_south().tilt_east()

    def spin_cycles(self, times):
        state = self
        for i in range(0, times):
            state = state.spin_cycle()
        return state

    def spin_cycles_with_cache(self, times):
        states = [self]
        state_by_str = {print_platform_state(self): 0}
        state = self
        repeats_at = 0
        for i in range(0, times):
            state = state.spin_cycle()
            state_str = print_platform_state(state)
            if state_str in state_by_str:
                repeats_at = state_by_str[state_str]
                break
            else:
                state_by_str[state_str] = i + 1
                states.append(state)
        repeating_len = len(states) - repeats_at
        remainder = (times - repeats_at) % repeating_len
        matching_index = repeats_at + remainder
        return states[matching_index]

    def get_spin_cycle_repeat(self):
        state_by_str = {print_platform_state(self): 0}
        state = self
        i = 0
        while True:
            state = state.spin_cycle()
            state_str = print_platform_state(state)
            i += 1
            if state_str in state_by_str:
                previous_i = state_by_str[state_str]
                return previous_i, i
            else:
                state_by_str[state_str] = i

    def total_load_on_north(self):
        total = 0
        for y, line in enumerate(self.lines):
            for tile in line:
                if tile == 'O':
                    total += self.height - y
        return total


def load_platform_state_from_file(input_file):
    with open(input_file, 'r') as file:
        return PlatformState(list(map(lambda line: list(line.strip()), file)))


def total_load_on_north_from_file(input_file):
    return load_platform_state_from_file(input_file).tilt_north().total_load_on_north()


def print_platform_state(state):
    out = io.StringIO()
    for line in state.lines:
        print(''.join(line), file=out)
    return out.getvalue()


def print_platform_states(states):
    out = io.StringIO()
    for state in states:
        print(print_platform_state(state), file=out)
    return out.getvalue()

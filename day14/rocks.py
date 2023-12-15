import io


class PlatformState:
    def __init__(self, lines):
        self.lines = lines
        self.height = len(self.lines)
        self.width = len(self.lines[0])

    def tilt_north(self):
        new_lines = self.lines.copy()
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
        new_lines = self.lines.copy()
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
        new_lines = self.lines.copy()
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
        new_lines = self.lines.copy()
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

    def total_load_on_north(self):
        height = len(self.lines)
        total = 0
        for y, line in enumerate(self.lines):
            for tile in line:
                if tile == 'O':
                    total += height - y
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

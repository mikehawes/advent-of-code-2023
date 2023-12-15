import io


class PlatformState:
    def __init__(self, lines):
        self.lines = lines

    def tilt_to_north(self):
        num_lines = len(self.lines)
        new_lines = self.lines.copy()
        for y in range(0, num_lines):
            new_line = []
            for x, tile in enumerate(new_lines[y]):
                new_tile = tile
                if tile == '.':
                    for y2 in range(y + 1, num_lines):
                        tile2 = new_lines[y2][x]
                        if tile2 == 'O':
                            new_tile = 'O'
                            new_lines[y2][x] = '.'
                            break
                        elif tile2 == '#':
                            break
                new_line.append(new_tile)
            new_lines[y] = new_line
        return PlatformState(new_lines)

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
    return load_platform_state_from_file(input_file).tilt_to_north().total_load_on_north()


def print_platform_state(state):
    out = io.StringIO()
    for line in state.lines:
        print(''.join(line), file=out)
    return out.getvalue()

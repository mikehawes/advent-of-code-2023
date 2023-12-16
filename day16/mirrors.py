class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)

    def find_max_energized_tiles_from_edge(self):
        max_energized = 0
        for x in range(0, self.width):
            energized_at_top = self.count_energized_tiles(beam=LightBeam(x, 0, 0, 1))
            energized_at_bottom = self.count_energized_tiles(beam=LightBeam(x, self.height - 1, 0, -1))
            max_energized = max(max_energized, energized_at_top, energized_at_bottom)
        for y in range(0, self.height):
            energized_at_left = self.count_energized_tiles(beam=LightBeam(0, y, 1, 0))
            energized_at_right = self.count_energized_tiles(beam=LightBeam(self.width - 1, y, -1, 0))
            max_energized = max(max_energized, energized_at_left, energized_at_right)
        return max_energized

    def count_energized_tiles(self, beam=None):
        if beam is None:
            beam = LightBeam(0, 0, 1, 0)
        beam_stack = [beam]
        beam_by_str = {}
        energized_by_pos = {}
        while beam_stack:
            beam = beam_stack.pop()
            energized_by_pos[beam.pos_str()] = True
            beam_str = beam.to_str()
            if beam_str in beam_by_str:
                continue
            beam_by_str[beam_str] = beam
            beam_stack.extend(beam.list_next(self))
        return len(energized_by_pos)


class LightBeam:
    def __init__(self, x, y, x_speed, y_speed):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed

    def to_str(self):
        return '{},{},{},{}'.format(self.x, self.y, self.x_speed, self.y_speed)

    def pos_str(self):
        return '{},{}'.format(self.x, self.y)

    def next(self, x_speed=None, y_speed=None):
        if x_speed is None:
            x_speed = self.x_speed
        if y_speed is None:
            y_speed = self.y_speed
        return LightBeam(self.x + x_speed, self.y + y_speed, x_speed, y_speed)

    def list_next(self, grid):
        y = self.y
        x = self.x
        tile = grid.lines[y][x]
        next_list = self.next_at_tile(tile)
        return list(filter(lambda beam: beam.is_on_grid(grid), next_list))

    def is_on_grid(self, grid):
        return 0 <= self.y < grid.height and 0 <= self.x < grid.width

    def next_at_tile(self, tile):
        match tile:
            case '|':
                if self.x_speed:
                    return [self.next(0, -1), self.next(0, 1)]
                else:
                    return [self.next()]
            case '-':
                if self.y_speed:
                    return [self.next(-1, 0), self.next(1, 0)]
                else:
                    return [self.next()]
            case '/':
                if self.x_speed > 0:
                    return [self.next(0, -1)]
                elif self.x_speed < 0:
                    return [self.next(0, 1)]
                elif self.y_speed > 0:
                    return [self.next(-1, 0)]
                elif self.y_speed < 0:
                    return [self.next(1, 0)]
            case '\\':
                if self.x_speed > 0:
                    return [self.next(0, 1)]
                elif self.x_speed < 0:
                    return [self.next(0, -1)]
                elif self.y_speed > 0:
                    return [self.next(1, 0)]
                elif self.y_speed < 0:
                    return [self.next(-1, 0)]
            case '.':
                return [self.next()]


def load_grid_from_file(input_file):
    with open(input_file, 'r') as file:
        return Grid(list(map(lambda line: line.strip(), file)))


def count_energized_tiles_in_file(input_file):
    grid = load_grid_from_file(input_file)
    return grid.count_energized_tiles()

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

    def list_next(self, lines):
        y = self.y
        x = self.x
        tile = lines[y][x]
        next_list = self.next_at_tile(tile)
        return list(filter(lambda beam: beam.is_on_grid(lines), next_list))

    def is_on_grid(self, lines):
        return 0 <= self.y < len(lines) and 0 <= self.x < len(lines[0])

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


def count_energized_tiles_in_file(input_file):
    with open(input_file, 'r') as file:
        lines = list(map(lambda line: line.strip(), file))

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
        beam_stack.extend(beam.list_next(lines))
    return len(energized_by_pos)

import io


class PlatformState:
    def __init__(self, lines):
        self.lines = lines

    def tilt_to_north(self):
        return self

    def total_load_on_north(self):
        return 0


def load_platform_state_from_file(input_file):
    with open(input_file, 'r') as file:
        return PlatformState(list(map(lambda line: line.strip(), file)))


def total_load_on_north_from_file(input_file):
    return load_platform_state_from_file(input_file).tilt_to_north().total_load_on_north()


def print_platform_state(state):
    out = io.StringIO()
    for line in state.lines:
        print(line, file=out)
    return out.getvalue()

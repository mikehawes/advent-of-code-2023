from day23.map import TrailsMap


def read_trails_from_file(input_file):
    with open(input_file, 'r') as file:
        return TrailsMap.from_lists(list(map(lambda line: list(line.strip()), file)))

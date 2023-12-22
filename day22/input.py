from day22.brick import Size, Location, SandBrick


def load_bricks_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_brick, enumerate(file)))


def read_brick(line_item):
    index, line = line_item
    parts = line.split('~')
    start = list(map(int, parts[0].split(',')))
    end = list(map(int, parts[1].split(',')))
    location = Location(start[0], start[1], start[2])
    length = Size(end[0] - start[0] + 1, end[1] - start[1] + 1, end[2] - start[2] + 1)
    return SandBrick(location, length, index)

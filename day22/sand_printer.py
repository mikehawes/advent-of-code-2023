import io

from day22.brick import Location, label_for_index, Size
from day22.snapshot import BricksSnapshot
from day22.structure import SupportStructure


def print_bricks_snapshot(snapshot: BricksSnapshot, layers=False):
    out = io.StringIO()
    if layers:
        adjacent = [
            print_bricks_layers(snapshot)
        ]
    else:
        adjacent = [
            print_bricks_snapshot_dimension(snapshot, 'x', 0, 1),
            print_bricks_snapshot_dimension(snapshot, 'y', 1, 0),
            print_bricks_by_z_value(snapshot)
        ]
    print_adjacent(adjacent, out)
    return out.getvalue()


def print_bricks_layers(snapshot: BricksSnapshot):
    out = io.StringIO()
    for z in range(snapshot.size.z - 1, 0, -1):
        print(str(z).rjust(3) + 'x'.center(snapshot.size.x).rstrip(), file=out)
        for y in range(0, snapshot.size.y):
            out.write('   ')
            for x in range(0, snapshot.size.x):
                location = Location(x, y, z)
                if location not in snapshot.bricks_by_location:
                    out.write('.')
                else:
                    brick = snapshot.bricks_by_location[location]
                    out.write(brick.label())
            if y == snapshot.size.y // 2:
                out.write(' y')
            print(file=out)
    return out.getvalue()


def print_bricks_snapshot_dimension(snapshot: BricksSnapshot, desc, dimension, other_dimension):
    out = io.StringIO()
    size_list = snapshot.size.as_list()
    size = size_list[dimension]
    other_size = size_list[other_dimension]
    print(desc.center(size).rstrip(), file=out)
    print(''.join(map(str, range(0, size))), file=out)
    for z in range(snapshot.size.z - 1, 0, -1):
        for value in range(0, size):
            indexes = {}
            for other in range(0, other_size):
                loc_list = [0, 0, z]
                loc_list[dimension] = value
                loc_list[other_dimension] = other
                loc = Location.from_list(loc_list)
                if loc in snapshot.bricks_by_location:
                    brick = snapshot.bricks_by_location[loc]
                    indexes[brick.index] = True
            num_bricks = len(indexes)
            if num_bricks > 1:
                out.write('?')
            elif num_bricks == 1:
                index = next(iter(indexes.keys()))
                out.write(label_for_index(index))
            else:
                out.write('.')
        out.write(' {}'.format(z))
        if z == snapshot.size.z // 2:
            out.write(' z')
        print(file=out)
    print('-' * size, '0', file=out)
    return out.getvalue()


def print_bricks_by_z_value(snapshot: BricksSnapshot):
    out = io.StringIO()
    print(file=out)
    print(file=out)
    structure = SupportStructure.from_snapshot(snapshot)
    for z in range(snapshot.size.z - 1, 0, -1):
        if z not in snapshot.bricks_by_min_z:
            print(file=out)
            continue
        bricks = snapshot.bricks_by_min_z[z]
        outputs = []
        for brick in bricks:
            would_fall = structure.which_bricks_would_fall(brick)
            outputs.append('{}{}<{} {} f{}>'.format(
                brick.label(), brick.index,
                print_location(brick.location),
                print_brick_size(brick.size),
                len(would_fall)))
        print(', '.join(outputs), file=out)
    return out.getvalue()


def print_location(location: Location):
    return ','.join(map(str, location.as_list()))


def print_brick_size(size: Size):
    if size.x > 1:
        return 'x{}'.format(size.x)
    elif size.y > 1:
        return 'y{}'.format(size.y)
    else:
        return 'z{}'.format(size.z)


def print_adjacent(printouts, out):
    widths = []
    printouts_lines = []
    max_length = 0
    for printout in printouts:
        printout_lines = printout.splitlines()
        printouts_lines.append(printout_lines)
        width = 0
        for line in printout_lines:
            width = max(width, len(line))
        widths.append(width)
        max_length = max(max_length, len(printout_lines))
    for i in range(0, max_length):
        parts = []
        for j in range(0, len(printouts)):
            printout_lines = printouts_lines[j]
            if i < len(printout_lines):
                line = printout_lines[i]
            else:
                line = ''
            parts.append(line.ljust(widths[j]))
        print('    '.join(parts).rstrip(), file=out)

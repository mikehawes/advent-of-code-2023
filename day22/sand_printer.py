import io

from day22.brick import Location, label_for_index, Size, SandBrick
from day22.fall import WhichBricksWouldFall
from day22.snapshot import BricksSnapshot
from day22.structure import SupportStructure
from util.print_adjacent import print_adjacent


def print_bricks_snapshot(snapshot: BricksSnapshot, layers=False):
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
    return print_adjacent(adjacent)


def print_bricks_layers(snapshot: BricksSnapshot):
    out = io.StringIO()
    structure = SupportStructure.from_snapshot(snapshot)
    would_fall = WhichBricksWouldFall.from_structure(structure)
    for z in range(snapshot.size.z - 1, 0, -1):
        for y in range(0, snapshot.size.y):
            if y == snapshot.size.y // 2:
                out.write(' y ')
            else:
                out.write('   ')
            y_bricks = []
            for x in range(0, snapshot.size.x):
                location = Location(x, y, z)
                if location not in snapshot.bricks_by_location:
                    if z > 1:
                        below = location.plus(z=-1)
                        if below in snapshot.bricks_by_location:
                            out.write('#')
                        else:
                            out.write('.')
                    else:
                        out.write('-')
                else:
                    brick = snapshot.bricks_by_location[location]
                    out.write(brick.label())
                    y_bricks.append(brick)
            if y_bricks:
                out.write('  ')
            printed = {}
            for brick in y_bricks:
                if brick.location in printed or brick.location.y != y:
                    continue
                out.write(' {}'.format(print_brick(brick, would_fall)))
                printed[brick.location] = True
            print(file=out)
        print(str(z).rjust(3) + 'x'.center(snapshot.size.x).rstrip(), file=out)
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
    would_fall = WhichBricksWouldFall.from_structure(structure)
    for z in range(snapshot.size.z - 1, 0, -1):
        if z not in snapshot.bricks_by_min_z:
            print(file=out)
            continue
        bricks = snapshot.bricks_by_min_z[z]
        outputs = []
        for brick in bricks:
            outputs.append(print_brick(brick, would_fall))
        print(', '.join(outputs), file=out)
    return out.getvalue()


def print_brick(brick: SandBrick, fall: WhichBricksWouldFall):
    would_fall = fall.which_bricks_would_fall(brick)
    return '{}{}<{} {} f{}>'.format(
        brick.label(), brick.index,
        print_location(brick.location),
        print_brick_size(brick.size),
        len(would_fall))


def print_location(location: Location):
    return ','.join(map(str, location.as_list()))


def print_brick_size(size: Size):
    if size.x > 1:
        return 'x{}'.format(size.x)
    elif size.y > 1:
        return 'y{}'.format(size.y)
    else:
        return 'z{}'.format(size.z)

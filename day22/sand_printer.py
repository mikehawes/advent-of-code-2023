import io

from day22.brick import Location, label_for_index
from day22.snapshot import BricksSnapshot


def print_bricks_snapshot(snapshot: BricksSnapshot):
    out = io.StringIO()
    x_view = print_bricks_snapshot_dimension(snapshot, 'x', 0, 1).splitlines()
    y_view = print_bricks_snapshot_dimension(snapshot, 'y', 1, 0).splitlines()
    x_width = 0
    for x_line in x_view:
        x_width = max(x_width, len(x_line))
    for i, x_line in enumerate(x_view):
        print(x_line.ljust(x_width), '  ', y_view[i], file=out)
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

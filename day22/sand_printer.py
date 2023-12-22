import io

from day22.brick import Location
from day22.snapshot import BricksSnapshot


def print_bricks_snapshot(snapshot: BricksSnapshot):
    out = io.StringIO()
    print_bricks_snapshot_dimension(snapshot, 'x', 0, 1, out)
    print_bricks_snapshot_dimension(snapshot, 'y', 1, 0, out)
    return out.getvalue()


def print_bricks_snapshot_dimension(snapshot: BricksSnapshot, desc, dimension, other_dimension, out):
    size_list = snapshot.size.as_list()
    size = size_list[dimension]
    other_size = size_list[other_dimension]
    print(desc.center(size).rstrip(), file=out)
    print(''.join(map(str, range(0, size))), file=out)
    for z in range(snapshot.size.z - 1, 0, -1):
        for value in range(0, size):
            other_filled = 0
            for other in range(0, other_size):
                loc_list = [0, 0, z]
                loc_list[dimension] = value
                loc_list[other_dimension] = other
                loc = Location.from_list(loc_list)
                if loc in snapshot.bricks_by_location:
                    other_filled += 1
            if other_filled > 0:
                out.write('#')
            else:
                out.write('.')
        out.write(' {}'.format(z))
        if z == snapshot.size.z // 2:
            out.write(' z')
        print(file=out)
    print('-' * size, '0', file=out)

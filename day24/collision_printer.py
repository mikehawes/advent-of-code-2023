import io

from day24.collision import list_2d_intersections
from day24.hail import Hailstone


def print_2d_intersections(hailstones: list[Hailstone]):
    out = io.StringIO()
    for intersection in list_2d_intersections(hailstones):
        print(print_hailstone(intersection.stone1), file=out)
        print(print_hailstone(intersection.stone2), file=out)
        if intersection.x is None:
            print("Hailstones' paths are parallel; they never intersect.", file=out)
        else:
            print("Hailstones' paths cross at x={:1.3f}, y={:1.3f}.".format(
                intersection.x, intersection.y), file=out)
        print(file=out)
    return out.getvalue()


def print_hailstone(hailstone: Hailstone):
    return 'Hailstone {}: {}, {}, {} @ {}, {}, {}'.format(
        hailstone.number,
        hailstone.position.x, hailstone.position.y, hailstone.position.z,
        hailstone.velocity.x, hailstone.velocity.y, hailstone.velocity.z)

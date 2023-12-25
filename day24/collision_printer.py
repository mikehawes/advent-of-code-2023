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
            print('Time for stone {}: {:1.3f}'.format(intersection.stone1.number, intersection.stone1_time), file=out)
            print('Time for stone {}: {:1.3f}'.format(intersection.stone2.number, intersection.stone2_time), file=out)
        print(file=out)
    return out.getvalue()


def print_3d_intersection_equations(hailstones: list[Hailstone]):
    out = io.StringIO()
    for hailstone in hailstones:
        print(print_hailstone(hailstone), file=out)
        p = hailstone.position.as_list()
        v = hailstone.velocity.as_list()
        for i in range(0, 3):
            for j in range(i + 1, 3):
                c1 = ['x', 'y', 'z'][i]
                c2 = ['x', 'y', 'z'][j]
                pc1 = v[j]
                pc2 = -v[i]
                vc1 = -p[j]
                vc2 = p[i]
                remaining = p[j] * v[i] - p[i] * v[j]
                print(f'{pc1}P{c1} {space_sign(pc2)}P{c2} + P{c2}V{c1} - P{c1}V{c2} '
                      f'{space_sign(vc1)}V{c1} {space_sign(vc2)}V{c2} {space_sign(remaining)} = 0', file=out)
    return out.getvalue()


def print_hailstone(hailstone: Hailstone):
    return 'Hailstone {}: {}, {}, {} @ {}, {}, {}'.format(
        hailstone.number,
        hailstone.position.x, hailstone.position.y, hailstone.position.z,
        hailstone.velocity.x, hailstone.velocity.y, hailstone.velocity.z)


def space_sign(value):
    if value >= 0:
        return '+ {}'.format(value)
    else:
        return '- {}'.format(abs(value))

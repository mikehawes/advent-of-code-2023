import io

from day24.collision_3d import first_equations_for_collisions
from day24.hail import Hailstone
from day24.intersection_2d import list_2d_intersections
from util.print_adjacent import print_adjacent


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


def print_3d_collision_equations(hailstones: list[Hailstone]):
    return print_adjacent([
        print_3d_intersection_first_equations(hailstones)
    ])


def print_3d_intersection_first_equations(hailstones: list[Hailstone]):
    out = io.StringIO()
    equations = first_equations_for_collisions(hailstones)
    last_hailstone = None
    for equation in equations:
        if equation.hailstone != last_hailstone:
            print(print_hailstone(equation.hailstone), file=out)
            last_hailstone = equation.hailstone

        c1 = ['x', 'y', 'z'][equation.coordinate_1]
        c2 = ['x', 'y', 'z'][equation.coordinate_2]
        pc1 = equation.position_c1
        pc2 = equation.position_c2
        vc1 = equation.velocity_c1
        vc2 = equation.velocity_c2
        print(f'{vc2}P{c1} {space_sign(-vc1)}P{c2} + P{c2}V{c1} - P{c1}V{c2} '
              f'{space_sign(-pc2)}V{c1} {space_sign(pc1)}V{c2} {space_sign(pc2 * vc1 - pc1 * vc2)} = 0', file=out)
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

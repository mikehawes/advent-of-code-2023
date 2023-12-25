import io

from day24.collision_3d import first_equations_for_collisions, Collision3DFirstEquation, \
    second_equations_for_collisions, Collision3DSecondEquation
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
    first_equations = first_equations_for_collisions(hailstones)
    second_equations = second_equations_for_collisions(hailstones, first_equations)
    return print_adjacent([
        print_3d_intersection_first_equations(hailstones, first_equations),
        print_3d_intersection_second_equations(second_equations)
    ])


def print_3d_intersection_first_equations(hailstones: list[Hailstone],
                                          equations: dict[int, list[Collision3DFirstEquation]]):
    out = io.StringIO()
    for hailstone in hailstones:
        print(print_hailstone(hailstone), file=out)
        for equation in equations[hailstone.number]:
            c1 = ['x', 'y', 'z'][equation.coordinate_1]
            c2 = ['x', 'y', 'z'][equation.coordinate_2]
            print(f'{equation.conjugate_p1}P{c1} {space_sign(equation.conjugate_p2)}P{c2} + P{c2}V{c1} - P{c1}V{c2} '
                  f'{space_sign(equation.conjugate_v1)}V{c1} {space_sign(equation.conjugate_v2)}V{c2} '
                  f'{space_sign(equation.remainder)} = 0', file=out)
    return out.getvalue()


def print_3d_intersection_second_equations(equations: list[Collision3DSecondEquation]):
    out = io.StringIO()
    for equation in equations:
        c1 = ['x', 'y', 'z'][equation.coordinate_1]
        c2 = ['x', 'y', 'z'][equation.coordinate_2]
        print(f'{equation.conjugate_p1}P{c1} {space_sign(equation.conjugate_p2)}P{c2} '
              f'{space_sign(equation.conjugate_v1)}V{c1} {space_sign(equation.conjugate_v2)}V{c2} '
              f'{space_sign(equation.remainder)} = 0', file=out)
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

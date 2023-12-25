from dataclasses import dataclass

from day24.hail import Hailstone


@dataclass
class Collision3DFirstEquation:
    coordinate_1: int
    coordinate_2: int
    conjugate_p1: float
    conjugate_p2: float
    conjugate_v1: float
    conjugate_v2: float
    remainder: float


@dataclass
class Collision3DSecondEquation:
    equation_1: Collision3DFirstEquation
    equation_2: Collision3DFirstEquation
    coordinate_1: int
    coordinate_2: int
    conjugate_p1: float
    conjugate_p2: float
    conjugate_v1: float
    conjugate_v2: float
    remainder: float

    @staticmethod
    def subtracting_equations(equation1: Collision3DFirstEquation, equation2: Collision3DFirstEquation):
        return Collision3DSecondEquation(equation1, equation2,
                                         coordinate_1=equation1.coordinate_1, coordinate_2=equation2.coordinate_2,
                                         conjugate_p1=equation2.conjugate_p1 - equation1.conjugate_p1,
                                         conjugate_p2=equation2.conjugate_p2 - equation1.conjugate_p2,
                                         conjugate_v1=equation2.conjugate_v1 - equation1.conjugate_v1,
                                         conjugate_v2=equation2.conjugate_v2 - equation1.conjugate_v2,
                                         remainder=equation2.remainder - equation1.remainder)


def first_equations_for_collisions(hailstones: list[Hailstone]) -> dict[int, list[Collision3DFirstEquation]]:
    equations = {}
    for hailstone in hailstones:
        p = hailstone.position.as_list()
        v = hailstone.velocity.as_list()
        stone_equations = []
        for c1 in range(0, 3):
            for c2 in range(c1 + 1, 3):
                stone_equations.append(Collision3DFirstEquation(
                    coordinate_1=c1, coordinate_2=c2,
                    conjugate_p1=v[c2], conjugate_p2=-v[c1],
                    conjugate_v1=-p[c2], conjugate_v2=p[c1],
                    remainder=p[c2] * v[c1] - p[c1] * v[c2]))
        equations[hailstone.number] = stone_equations
    return equations


def second_equations_for_collisions(
        hailstones: list[Hailstone],
        first_equations: dict[int, list[Collision3DFirstEquation]]) \
        -> list[Collision3DSecondEquation]:
    equations = []
    for i in range(0, len(hailstones) - 1):
        stone1 = hailstones[i]
        stone2 = hailstones[i + 1]
        firsts1 = first_equations[stone1.number]
        firsts2 = first_equations[stone2.number]
        for j in range(0, len(firsts1)):
            equations.append(Collision3DSecondEquation.subtracting_equations(firsts1[j], firsts2[j]))
    return equations

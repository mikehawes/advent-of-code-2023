from dataclasses import dataclass

from day24.hail import Hailstone


@dataclass
class Collision3DFirstEquation:
    coordinate_1: int
    coordinate_2: int
    position_c1: float
    position_c2: float
    velocity_c1: float
    velocity_c2: float


class Collision3DSecondEquation:
    equation_1: Collision3DFirstEquation
    equation_2: Collision3DFirstEquation


def first_equations_for_collisions(hailstones: list[Hailstone]) -> dict[int, list[Collision3DFirstEquation]]:
    equations = {}
    for hailstone in hailstones:
        p = hailstone.position.as_list()
        v = hailstone.velocity.as_list()
        stone_equations = []
        for i in range(0, 3):
            for j in range(i + 1, 3):
                stone_equations.append(Collision3DFirstEquation(
                    coordinate_1=i, coordinate_2=j,
                    position_c1=p[i], position_c2=p[j],
                    velocity_c1=v[i], velocity_c2=v[j]))
        equations[hailstone.number] = stone_equations
    return equations


def second_equations(hailstones: list[Hailstone], first_equations: dict[int, list[Collision3DFirstEquation]]):
    pass

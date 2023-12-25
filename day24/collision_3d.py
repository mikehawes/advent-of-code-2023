from dataclasses import dataclass

from day24.hail import Hailstone


@dataclass
class Collision3DFirstEquation:
    hailstone: Hailstone
    coordinate_1: int
    coordinate_2: int
    position_c1: float
    position_c2: float
    velocity_c1: float
    velocity_c2: float


def first_equations_for_collisions(hailstones: list[Hailstone]) -> list[Collision3DFirstEquation]:
    equations = []
    for hailstone in hailstones:
        p = hailstone.position.as_list()
        v = hailstone.velocity.as_list()
        for i in range(0, 3):
            for j in range(i + 1, 3):
                equations.append(Collision3DFirstEquation(
                    hailstone=hailstone, coordinate_1=i, coordinate_2=j,
                    position_c1=p[i], position_c2=p[j],
                    velocity_c1=v[i], velocity_c2=v[j]))
    return equations

from dataclasses import dataclass

import numpy as np

from day24.hail import Hailstone, Position, Velocity


@dataclass
class Collision3DFirstEquation:
    coordinate_1: int
    coordinate_2: int
    coefficient_p1: float
    coefficient_p2: float
    coefficient_v1: float
    coefficient_v2: float
    ordinate: float


@dataclass
class Collision3DSecondEquation:
    equation_1: Collision3DFirstEquation
    equation_2: Collision3DFirstEquation
    coordinate_1: int
    coordinate_2: int
    coefficient_p1: float
    coefficient_p2: float
    coefficient_v1: float
    coefficient_v2: float
    ordinate: float

    @staticmethod
    def subtracting_equations(equation1: Collision3DFirstEquation, equation2: Collision3DFirstEquation):
        return Collision3DSecondEquation(equation1, equation2,
                                         coordinate_1=equation1.coordinate_1, coordinate_2=equation2.coordinate_2,
                                         coefficient_p1=equation2.coefficient_p1 - equation1.coefficient_p1,
                                         coefficient_p2=equation2.coefficient_p2 - equation1.coefficient_p2,
                                         coefficient_v1=equation2.coefficient_v1 - equation1.coefficient_v1,
                                         coefficient_v2=equation2.coefficient_v2 - equation1.coefficient_v2,
                                         ordinate=equation2.ordinate - equation1.ordinate)

    def coefficients_list(self) -> list[float]:
        p_coefficients = [0.0, 0.0, 0.0]
        v_coefficients = [0.0, 0.0, 0.0]
        p_coefficients[self.coordinate_1] = self.coefficient_p1
        p_coefficients[self.coordinate_2] = self.coefficient_p2
        v_coefficients[self.coordinate_1] = self.coefficient_v1
        v_coefficients[self.coordinate_2] = self.coefficient_v2
        return p_coefficients + v_coefficients


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
                    coefficient_p1=v[c2], coefficient_p2=-v[c1],
                    coefficient_v1=-p[c2], coefficient_v2=p[c1],
                    ordinate=p[c2] * v[c1] - p[c1] * v[c2]))
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


def solve_collision_equations(equations: list[Collision3DSecondEquation]) -> tuple[Position, Velocity]:
    coefficients_arrays = np.array(list(map(lambda e: e.coefficients_list(), equations)))
    ordinates = np.array(list(map(lambda e: -e.ordinate, equations)))
    results = list(map(lambda value: round(value, 2), np.linalg.lstsq(coefficients_arrays, ordinates)[0]))
    return Position(results[0], results[1], results[2]), Velocity(results[3], results[4], results[5])

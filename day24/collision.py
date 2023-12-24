from dataclasses import dataclass

from day24.hail import Hailstone, Position


@dataclass
class Intersection2D:
    stone1: Hailstone
    stone2: Hailstone
    x: float | None
    y: float | None


def count_2d_intersections_in_area(hailstones: list[Hailstone], min_position: Position, max_position: Position):
    pass


def list_2d_intersections(hailstones: list[Hailstone]):
    intersections = []
    for i in range(0, len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            stone1 = hailstones[i]
            stone2 = hailstones[j]
            x, y = find_2d_intersection(stone1, stone2)
            intersections.append(Intersection2D(stone1, stone2, x, y))
    return intersections


def find_2d_intersection(stone1: Hailstone, stone2: Hailstone):
    x0 = stone1.position.x
    y0 = stone1.position.y
    dx = stone1.velocity.x
    dy = stone1.velocity.y
    a0 = stone2.position.x
    b0 = stone2.position.y
    da = stone2.velocity.x
    db = stone2.velocity.y
    if dx / dy == da / db:
        return None, None
    x = (b0 - y0 + x0 * dy / dx - a0 * db / da) / (dy / dx - db / da)
    y = (a0 - x0 + y0 * dx / dy - b0 * da / db) / (dx / dy - da / db)
    return x, y

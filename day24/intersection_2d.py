from dataclasses import dataclass

from day24.hail import Hailstone, Position


@dataclass
class Intersection2D:
    stone1: Hailstone
    stone2: Hailstone
    x: float | None
    y: float | None
    stone1_time: float | None
    stone2_time: float | None


def count_2d_intersections_in_area(hailstones: list[Hailstone], min_position: Position, max_position: Position):
    num_intersections = 0
    for intersection in list_2d_intersections(hailstones):
        if intersection.x is None or intersection.stone1_time < 0 or intersection.stone2_time < 0:
            continue
        if min_position.x <= intersection.x <= max_position.x and min_position.y <= intersection.y <= max_position.y:
            num_intersections += 1
    return num_intersections


def list_2d_intersections(hailstones: list[Hailstone]):
    intersections = []
    for i in range(0, len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            stone1 = hailstones[i]
            stone2 = hailstones[j]
            intersections.append(find_2d_intersection(stone1, stone2))
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
        return Intersection2D(stone1, stone2, None, None, None, None)
    x = (b0 - y0 + x0 * dy / dx - a0 * db / da) / (dy / dx - db / da)
    y = (a0 - x0 + y0 * dx / dy - b0 * da / db) / (dx / dy - da / db)
    t1 = (x - x0) / dx
    t2 = (x - a0) / da
    return Intersection2D(stone1, stone2, x, y, t1, t2)

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Position:
    x: Decimal
    y: Decimal
    z: Decimal

    @staticmethod
    def from_list(coordinates: list[Decimal]):
        return Position(coordinates[0], coordinates[1], coordinates[2])

    @staticmethod
    def all(value: Decimal):
        return Position(value, value, value)

    def as_list(self) -> list[Decimal]:
        return [self.x, self.y, self.z]


@dataclass(frozen=True)
class Velocity:
    x: Decimal
    y: Decimal
    z: Decimal

    @staticmethod
    def from_list(speeds: list[Decimal]):
        return Velocity(speeds[0], speeds[1], speeds[2])

    def as_list(self) -> list[Decimal]:
        return [self.x, self.y, self.z]


@dataclass
class Hailstone:
    number: int
    position: Position
    velocity: Velocity


def load_hailstones_from_file(input_file) -> list[Hailstone]:
    with open(input_file, 'r') as file:
        return list(map(read_hailstone_line, enumerate(file)))


def read_hailstone_line(item: tuple[int, str]) -> Hailstone:
    number, line = item
    parts = line.split('@')
    position = list(map(lambda coordinate: Decimal(coordinate.strip()), parts[0].split(',')))
    velocity = list(map(lambda speed: Decimal(speed.strip()), parts[1].split(',')))
    return Hailstone(number, Position.from_list(position), Velocity.from_list(velocity))

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int
    z: int

    @staticmethod
    def from_list(coordinates: list[int]):
        return Position(coordinates[0], coordinates[1], coordinates[2])

    @staticmethod
    def all(value: int):
        return Position(value, value, value)


@dataclass(frozen=True)
class Velocity:
    x: int
    y: int
    z: int

    @staticmethod
    def from_list(speeds: list[int]):
        return Velocity(speeds[0], speeds[1], speeds[2])


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
    position = list(map(lambda coordinate: int(coordinate.strip()), parts[0].split(',')))
    velocity = list(map(lambda speed: int(speed.strip()), parts[1].split(',')))
    return Hailstone(number, Position.from_list(position), Velocity.from_list(velocity))

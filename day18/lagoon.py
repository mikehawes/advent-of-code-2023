from dataclasses import dataclass

from day18.instruction import DigInstruction


@dataclass(frozen=True)
class Location:
    x: int
    y: int

    def next_in_direction(self, direction):
        match direction:
            case 'L':
                return Location(self.x - 1, self.y)
            case 'R':
                return Location(self.x + 1, self.y)
            case 'U':
                return Location(self.x, self.y - 1)
            case 'D':
                return Location(self.x, self.y + 1)


@dataclass(frozen=True)
class LagoonTile:
    contents: str
    instruction: DigInstruction | None


@dataclass(frozen=True)
class Lagoon:
    lines: list[list[LagoonTile]]

    def __str__(self):
        return '\n'.join(map(
            lambda line: ''.join(map(
                lambda tile: tile.contents,
                line)),
            self.lines))


def dig_lagoon(instructions: list[DigInstruction]):
    location = Location(0, 0)
    tiles_by_location = {location: LagoonTile('#', None)}
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for instruction in instructions:
        for i in range(0, instruction.distance):
            location = location.next_in_direction(instruction.direction)
            tiles_by_location[location] = LagoonTile('#', instruction)
        min_x = min(min_x, location.x)
        max_x = max(max_x, location.x)
        min_y = min(min_y, location.y)
        max_y = max(max_y, location.y)

    lines = []
    for y in range(min_y, max_y + 1):
        line = []
        lines.append(line)
        for x in range(min_x, max_x + 1):
            location = Location(x, y)
            if location in tiles_by_location:
                line.append(tiles_by_location[location])
            else:
                if is_internal_location(location, tiles_by_location, max_x):
                    line.append(LagoonTile('#', None))
                else:
                    line.append(LagoonTile('.', None))
    return Lagoon(lines)


def is_internal_location(location, tiles_by_location: dict[Location, LagoonTile], max_x):
    winding_number = 0
    for x in range(location.x, max_x + 1):
        test = Location(x, location.y)
        if test in tiles_by_location:
            tile = tiles_by_location[test]
            if tile.instruction and tile.instruction.is_up_or_down():
                winding_number += 1
    return winding_number % 2 == 1

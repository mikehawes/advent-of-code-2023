import io
import re
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
    instruction: DigInstruction | None = None


@dataclass(frozen=True)
class Lagoon:
    lines: list[list[LagoonTile]]
    capacity: int

    def __str__(self):
        out = io.StringIO()
        print('Capacity:', self.capacity, file=out)
        for line in self.lines:
            for tile in line:
                out.write(tile.contents)
            print(file=out)
        return out.getvalue()


def dig_lagoon(instructions: list[DigInstruction]):
    location = Location(0, 0)
    tiles_by_location = {location: LagoonTile('#')}
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for i, instruction in enumerate(instructions):
        next_instruction = instructions[0] if i == len(instructions) - 1 else instructions[i + 1]
        for j in range(0, instruction.distance):
            location = location.next_in_direction(instruction.direction)
            contents = instruction.contents_at_offset(j, next_instruction)
            tiles_by_location[location] = LagoonTile(contents, instruction)
        min_x = min(min_x, location.x)
        max_x = max(max_x, location.x)
        min_y = min(min_y, location.y)
        max_y = max(max_y, location.y)

    lines = []
    capacity = 0
    for y in range(min_y, max_y + 1):
        line = []
        lines.append(line)
        for x in range(min_x, max_x + 1):
            location = Location(x, y)
            if location in tiles_by_location:
                line.append(tiles_by_location[location])
                capacity += 1
            else:
                if is_internal_location(location, tiles_by_location, max_x):
                    line.append(LagoonTile('#'))
                    capacity += 1
                else:
                    line.append(LagoonTile('.'))
    return Lagoon(lines, capacity)


def is_internal_location(location, tiles_by_location: dict[Location, LagoonTile], max_x):
    line = []
    for x in range(location.x, max_x + 1):
        test = Location(x, location.y)
        if test in tiles_by_location:
            line.append(tiles_by_location[test].contents)
        else:
            line.append('.')
    line = ''.join(line)
    winding_number = len(re.findall(r'║|╚═*╗|╔═*╝', line))
    return winding_number % 2 == 1

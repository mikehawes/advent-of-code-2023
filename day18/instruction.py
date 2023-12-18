import re
from dataclasses import dataclass


@dataclass(frozen=True)
class DigInstruction:
    direction: str
    distance: int
    colour_code: str

    def is_up_or_down(self):
        return self.direction == 'U' or self.direction == 'D'

    def contents_at_offset(self, offset, next_instruction):
        if offset == self.distance - 1 and next_instruction:
            return contents_at_direction_change(self.direction, next_instruction.direction)
        return contents_for_direction(self.direction)


def read_dig_instructions_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_dig_instruction_line, file))


def read_dig_instruction_line(line):
    match = re.match(r'([LRUD]) ([0-9]+) \((#.+)\)', line)
    if match:
        return DigInstruction(match.group(1), int(match.group(2)), match.group(3))
    else:
        return None


def contents_at_direction_change(before, after):
    match before:
        case 'L':
            match after:
                case 'U':
                    return '╚'
                case 'D':
                    return '╔'
        case 'R':
            match after:
                case 'U':
                    return '╝'
                case 'D':
                    return '╗'
        case 'U':
            match after:
                case 'L':
                    return '╗'
                case 'R':
                    return '╔'
        case 'D':
            match after:
                case 'L':
                    return '╝'
                case 'R':
                    return '╚'


def contents_for_direction(direction):
    match direction:
        case 'L' | 'R':
            return '═'
        case 'U' | 'D':
            return '║'

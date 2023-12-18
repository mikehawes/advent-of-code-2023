import re
from dataclasses import dataclass


def read_dig_instruction_line(line):
    match = re.match(r'([LRUD]) ([0-9]+) \((#.+)\)', line)
    if match:
        return DigInstruction(match.group(1), int(match.group(2)), match.group(3))
    else:
        return None


def read_dig_instructions_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_dig_instruction_line, file))


@dataclass
class DigInstruction:
    direction: str
    distance: int
    colour_code: str

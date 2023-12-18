import re
from dataclasses import dataclass


@dataclass(frozen=True)
class DigInstruction:
    direction: str
    distance: int
    colour_code: str

    def is_up_or_down(self):
        return self.direction == 'U' or self.direction == 'D'


def read_dig_instructions_from_file(input_file):
    with open(input_file, 'r') as file:
        return list(map(read_dig_instruction_line, file))


def read_dig_instruction_line(line):
    match = re.match(r'([LRUD]) ([0-9]+) \((#.+)\)', line)
    if match:
        return DigInstruction(match.group(1), int(match.group(2)), match.group(3))
    else:
        return None

import re


def get_input():
    return open('input', 'r')


def get_gear_part_numbers(gear_index):
    gear_part_numbers = get_gear_part_numbers_on_line(part_numbers_by_line[line_index], gear_index)
    if line_index > 0:
        gear_part_numbers.extend(get_gear_part_numbers_on_line(part_numbers_by_line[line_index-1], gear_index))
    if line_index + 1 < len(part_numbers_by_line):
        gear_part_numbers.extend(get_gear_part_numbers_on_line(part_numbers_by_line[line_index+1], gear_index))
    return gear_part_numbers


def get_gear_part_numbers_on_line(part_number_matches, gear_index):
    part_numbers_on_line = []
    for part_number in part_number_matches:
        span = part_number.span()
        if span[0] - 1 <= gear_index <= span[1]:
            part_numbers_on_line.append(int(part_number.group(0)))
    return part_numbers_on_line


part_numbers_by_line = {}
line_index = 0
for line in get_input():
    line_part_numbers = []
    for number in re.finditer(r"[0-9]+", line):
        line_part_numbers.append(number)
    part_numbers_by_line[line_index] = line_part_numbers
    line_index += 1

print(part_numbers_by_line)

gear_ratios = []
line_index = 0
for line in get_input():
    for gear in re.finditer(r"\*", line):
        part_numbers = get_gear_part_numbers(gear.start())
        if len(part_numbers) == 2:
            gear_ratios.append(part_numbers[0] * part_numbers[1])
    line_index += 1

print(gear_ratios)
print(sum(gear_ratios))

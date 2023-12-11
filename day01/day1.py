import re


def parse_digit(digit):
    match digit:
        case 'one':
            return '1'
        case 'two':
            return '2'
        case 'three':
            return '3'
        case 'four':
            return '4'
        case 'five':
            return '5'
        case 'six':
            return '6'
        case 'seven':
            return '7'
        case 'eight':
            return '8'
        case 'nine':
            return '9'
        case _:
            return digit


total = 0
for line in open('input', 'r'):
    digits = re.findall('(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))', line)
    if digits:
        print(digits)
        value = int(parse_digit(digits[0]) + parse_digit(digits[-1]))
        total += value

print('Total: {}'.format(total))

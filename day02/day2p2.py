import re


games_sum = 0
for line in open('input', 'r'):
    game = int(re.search('Game ([0-9]+):', line).group(1))
    max_by_colour = {
        'red': 0,
        'green': 0,
        'blue': 0
    }
    for pull in re.finditer('(([0-9]+) (red|green|blue)(, )?)+(;|$)', line):
        for pull_colour in re.finditer('([0-9]+) (red|green|blue)', pull.group(0)):
            count = int(pull_colour.group(1))
            colour = pull_colour.group(2)
            if count > max_by_colour[colour]:
                max_by_colour[colour] = count
    power = max_by_colour['red'] * max_by_colour['green'] * max_by_colour['blue']
    games_sum += power

print(games_sum)

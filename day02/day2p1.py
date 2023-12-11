import re


max_by_colour = {
    'red': 12,
    'green': 13,
    'blue': 14
}
games_sum = 0
for line in open('input', 'r'):
    game = int(re.search('Game ([0-9]+):', line).group(1))
    game_is_possible = True
    for pull in re.finditer('(([0-9]+) (red|green|blue)(, )?)+(;|$)', line):
        for pull_colour in re.finditer('([0-9]+) (red|green|blue)', pull.group(0)):
            count = int(pull_colour.group(1))
            colour = pull_colour.group(2)
            if count > max_by_colour[colour]:
                game_is_possible = False
    if game_is_possible:
        games_sum += game

print(games_sum)

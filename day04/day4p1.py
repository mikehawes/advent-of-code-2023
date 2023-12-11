import re


def get_input():
    return open('input', 'r')


def numbers(section):
    return list(map(lambda n: n.group(0), re.finditer('[0-9]+', section)))


score = 0
for line in get_input():
    card_match = re.match(r"Card\s+([0-9]+): ", line)
    card = card_match.group(1)
    sections = line[card_match.span()[1]:].split("|")
    winning_numbers = numbers(sections[0])
    playing_numbers = numbers(sections[1])
    card_score = 0
    for number in playing_numbers:
        if number in winning_numbers:
            if card_score == 0:
                card_score = 1
            else:
                card_score *= 2
    print('Card {}, winning {}, playing {}, score {}'.format(card, winning_numbers, playing_numbers, card_score))
    score += card_score

print('Score: {}'.format(score))

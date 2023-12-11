import re


def get_input():
    return open('input', 'r')


def numbers(section):
    return list(map(lambda n: n.group(0), re.finditer('[0-9]+', section)))


scratchcards = 0
bonus_copies_by_card = {}
for line in get_input():
    card_match = re.match(r"Card\s+([0-9]+): ", line)
    card = int(card_match.group(1))
    instances = 1
    if card in bonus_copies_by_card:
        instances += bonus_copies_by_card[card]
    sections = line[card_match.span()[1]:].split("|")
    winning_numbers = numbers(sections[0])
    playing_numbers = numbers(sections[1])
    card_wins = 0
    for number in playing_numbers:
        if number in winning_numbers:
            card_wins += 1
    print('Card {}, winning {}, playing {}, {} winning numbers, {} instances'
          .format(card, winning_numbers, playing_numbers, card_wins, instances))
    for i in range(0, card_wins):
        bonus_card = card + i + 1
        if bonus_card in bonus_copies_by_card:
            bonus_copies_by_card[bonus_card] += instances
        else:
            bonus_copies_by_card[bonus_card] = instances
        print('Bonus copies of {}: {}'.format(bonus_card, bonus_copies_by_card[bonus_card]))
    scratchcards += instances

print('Scratchcards: {}'.format(scratchcards))

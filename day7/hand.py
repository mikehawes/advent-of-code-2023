import functools

value_by_card_no_joker = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

value_by_card_with_joker = {
    'J': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'Q': 11,
    'K': 12,
    'A': 13
}


@functools.total_ordering
class Hand:
    def __init__(self, cards, value_by_card=None, use_jokers=False):
        if value_by_card is None:
            value_by_card = value_by_card_no_joker
        self.cards = cards
        self.card_values = list(map(lambda c: value_by_card[c], cards))
        self.count_by_card = {}
        for card in cards:
            if card in self.count_by_card:
                self.count_by_card[card] += 1
            else:
                self.count_by_card[card] = 1
        if use_jokers and 'J' in self.count_by_card:
            num_jokers = self.count_by_card['J']
            del self.count_by_card['J']
            if self.count_by_card:
                most_frequent_card = max(self.count_by_card, key=lambda c: self.count_by_card[c])
                self.count_by_card[most_frequent_card] += num_jokers
            else:
                self.count_by_card['J'] = num_jokers
        counts = self.count_by_card.values()
        match (max(counts)):
            case 1:
                self.value = 1
            case 2:
                num_pairs = 0
                for count in counts:
                    if count == 2:
                        num_pairs += 1
                self.value = num_pairs + 1
            case 3:
                self.value = 4
                for count in counts:
                    if count == 2:
                        self.value = 5
            case 4:
                self.value = 6
            case 5:
                self.value = 7

    @staticmethod
    def from_cards(cards):
        return Hand(cards, value_by_card_no_joker, False)

    @staticmethod
    def from_cards_with_joker(cards):
        return Hand(cards, value_by_card_with_joker, True)

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.value < other.value:
            return True
        if self.value > other.value:
            return False
        for i in range(0, len(self.cards)):
            my_card = self.card_values[i]
            other_card = other.card_values[i]
            if my_card < other_card:
                return True
            if my_card > other_card:
                return False
        return False

    def __repr__(self):
        return '{} (value {})'.format(self.cards, self.value)

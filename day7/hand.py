import functools

value_by_card = {
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


@functools.total_ordering
class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.count_by_card = {}
        for card in cards:
            if card in self.count_by_card:
                self.count_by_card[card] += 1
            else:
                self.count_by_card[card] = 1
        counts = self.count_by_card.values()
        match(max(counts)):
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

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.value < other.value:
            return True
        if self.value > other.value:
            return False
        for i in range(0, len(self.cards)):
            my_card = value_by_card[self.cards[i]]
            other_card = value_by_card[other.cards[i]]
            if my_card < other_card:
                return True
            if my_card > other_card:
                return False
        return False

    def __repr__(self):
        return '{} (value {})'.format(self.cards, self.value)

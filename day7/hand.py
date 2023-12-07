import functools


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
            if self.cards[i] < other.cards[i]:
                return True
        return False

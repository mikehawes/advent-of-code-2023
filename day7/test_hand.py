import unittest

from day7.hand import Hand


def hand(cards):
    return Hand.from_cards(cards)


def with_joker(cards):
    return Hand.from_cards_with_joker(cards)


class TestCompareHandByType(unittest.TestCase):

    def test_should_find_high_card_is_less_than_one_pair(self):
        self.assertLess(hand("23456"), hand("A23A4"))

    def test_should_find_one_pair_is_less_than_two_pair(self):
        self.assertLess(hand("A23A4"), hand("23432"))

    def test_should_find_two_pair_is_less_than_three_of_a_kind(self):
        self.assertLess(hand("23432"), hand("TTT98"))

    def test_should_find_three_of_a_kind_is_less_than_full_house(self):
        self.assertLess(hand("TTT98"), hand("23332"))

    def test_should_find_full_house_is_less_than_four_of_a_kind(self):
        self.assertLess(hand("23332"), hand("AA8AA"))

    def test_should_find_four_of_a_kind_is_less_than_five_of_a_kind(self):
        self.assertLess(hand("AA8AA"), hand("AAAAA"))


class TestCompareHandByCardValue(unittest.TestCase):

    def test_should_find_hand_stronger_by_first_card(self):
        self.assertGreater(hand("33332"), hand("2AAAA"))

    def test_should_find_hand_stronger_by_third_card(self):
        self.assertGreater(hand("77888"), hand("77788"))

    def test_should_find_ten_stronger_than_nine(self):
        self.assertGreater(hand("T2222"), hand("92222"))

    def test_should_find_jack_stronger_than_ten(self):
        self.assertGreater(hand("J2222"), hand("T2222"))

    def test_should_find_queen_stronger_than_jack(self):
        self.assertGreater(hand("Q2222"), hand("J2222"))

    def test_should_find_king_stronger_than_queen(self):
        self.assertGreater(hand("K2222"), hand("Q2222"))

    def test_should_find_ace_stronger_than_king(self):
        self.assertGreater(hand("A2222"), hand("K2222"))

    def test_should_find_first_card_stronger_regardless_of_compare_order(self):
        self.assertGreater(hand("T75Q2"), hand("936A5"))
        self.assertLess(hand("936A5"), hand("T75Q2"))


class TestApplyJoker(unittest.TestCase):

    def test_should_find_joker_weaker_for_same_hand(self):
        self.assertLess(with_joker("J2222"), with_joker("22222"))

    def test_should_find_hand_stronger_when_joker_turns_hand_into_five_of_a_kind(self):
        self.assertGreater(with_joker("J2222"), with_joker("32222"))

    def test_should_find_five_jokers_stronger_than_four_of_a_kind(self):
        self.assertGreater(with_joker("JJJJJ"), with_joker("32222"))

    def test_should_find_five_jokers_weaker_than_other_five_of_a_kind(self):
        self.assertLess(with_joker("JJJJJ"), with_joker("22222"))

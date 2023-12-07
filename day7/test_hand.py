import unittest

from day7.hand import Hand


class TestCompareHandByType(unittest.TestCase):

    def test_should_find_high_card_is_less_than_one_pair(self):
        self.assertLess(Hand("23456"), Hand("A23A4"))

    def test_should_find_one_pair_is_less_than_two_pair(self):
        self.assertLess(Hand("A23A4"), Hand("23432"))

    def test_should_find_two_pair_is_less_than_three_of_a_kind(self):
        self.assertLess(Hand("23432"), Hand("TTT98"))

    def test_should_find_three_of_a_kind_is_less_than_full_house(self):
        self.assertLess(Hand("TTT98"), Hand("23332"))

    def test_should_find_full_house_is_less_than_four_of_a_kind(self):
        self.assertLess(Hand("23332"), Hand("AA8AA"))

    def test_should_find_four_of_a_kind_is_less_than_five_of_a_kind(self):
        self.assertLess(Hand("AA8AA"), Hand("AAAAA"))


class TestCompareHandByCardValue(unittest.TestCase):

    def test_should_find_hand_stronger_by_first_card(self):
        self.assertLess(Hand("2AAAA"), Hand("33332"))

    def test_should_find_hand_stronger_by_third_card(self):
        self.assertLess(Hand("77788"), Hand("77888"))

    def test_should_find_ten_stronger_than_nine(self):
        self.assertLess(Hand("92222"), Hand("T2222"))

    def test_should_find_jack_stronger_than_ten(self):
        self.assertLess(Hand("T2222"), Hand("J2222"))

    def test_should_find_queen_stronger_than_jack(self):
        self.assertLess(Hand("J2222"), Hand("Q2222"))

    def test_should_find_king_stronger_than_queen(self):
        self.assertLess(Hand("Q2222"), Hand("K2222"))

    def test_should_find_ace_stronger_than_king(self):
        self.assertLess(Hand("K2222"), Hand("A2222"))

    def test_should_find_first_card_stronger_regardless_of_compare_order(self):
        self.assertLess(Hand("936A5"), Hand("T75Q2"))
        self.assertGreater(Hand("T75Q2"), Hand("936A5"))

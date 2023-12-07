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

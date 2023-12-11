import unittest

from day07.day7p1p2 import get_total_winnings_for_hands
from day07.hand import Hand


class TestDay7Part1(unittest.TestCase):

    def test_should_get_total_winnings_for_example(self):
        self.assertEqual(6440, get_total_winnings_for_hands('example'))

    def test_should_get_total_winnings_for_input(self):
        self.assertEqual(248422077, get_total_winnings_for_hands('input'))


class TestDay7Part2(unittest.TestCase):

    def test_should_get_total_winnings_for_example(self):
        self.assertEqual(5905, get_total_winnings_for_hands('example', Hand.from_cards_with_jokers))

    def test_should_get_total_winnings_for_input(self):
        self.assertEqual(249817836, get_total_winnings_for_hands('input', Hand.from_cards_with_jokers))

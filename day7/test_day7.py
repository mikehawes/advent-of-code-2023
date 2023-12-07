import unittest

from day7.day7p1 import get_total_winnings_for_hands


class TestDay7Part1(unittest.TestCase):

    def test_should_get_total_winnings_for_example(self):
        self.assertEqual(6440, get_total_winnings_for_hands('example'))

    def test_should_get_total_winnings_for_input(self):
        self.assertEqual(248422077, get_total_winnings_for_hands('input'))

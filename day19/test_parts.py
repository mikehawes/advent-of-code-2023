import unittest

from day19.parts import ScoreRange, remove_overlaps


class TestParts(unittest.TestCase):

    def test_should_remove_exact_overlap(self):
        self.assertEqual([ScoreRange(1, 10)],
                         remove_overlaps([ScoreRange(1, 5), ScoreRange(6, 10)]))

    def test_should_remove_unsorted_overlap(self):
        self.assertEqual([ScoreRange(1, 10)],
                         remove_overlaps([ScoreRange(4, 10), ScoreRange(1, 5)]))

    def test_should_remove_overlap_from_middle(self):
        self.assertEqual([ScoreRange(1, 10)],
                         remove_overlaps([ScoreRange(1, 5), ScoreRange(2, 10), ScoreRange(3, 5)]))

    def test_should_keep_separation(self):
        self.assertEqual([ScoreRange(1, 4), ScoreRange(6, 10)],
                         remove_overlaps([ScoreRange(1, 4), ScoreRange(6, 10)]))

    def test_should_merge_some(self):
        self.assertEqual([ScoreRange(1, 4), ScoreRange(6, 10)],
                         remove_overlaps([ScoreRange(1, 4), ScoreRange(6, 8), ScoreRange(9, 10)]))

    def test_should_remove_invalid_range(self):
        self.assertEqual([],
                         remove_overlaps([ScoreRange(2, 1)]))

    def test_should_remove_invalid_range_from_middle(self):
        self.assertEqual([ScoreRange(1, 2), ScoreRange(8, 10)],
                         remove_overlaps([ScoreRange(1, 2), ScoreRange(4, 3), ScoreRange(8, 10)]))

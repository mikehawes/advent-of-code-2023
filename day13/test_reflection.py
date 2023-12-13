import unittest

from day13.reflection import compute_reflections_number_from_file, unsmudge_and_compute_reflections_number_from_file


class TestReflections(unittest.TestCase):

    def test_should_answer_example(self):
        self.assertEqual(405, compute_reflections_number_from_file('example'))

    def test_should_answer_input(self):
        self.assertEqual(30158, compute_reflections_number_from_file('input'))

    def test_should_unsmudge_and_answer_example(self):
        self.assertEqual(400, unsmudge_and_compute_reflections_number_from_file('example'))

    def test_should_unsmudge_and_answer_input(self):
        self.assertEqual(36474, unsmudge_and_compute_reflections_number_from_file('input'))

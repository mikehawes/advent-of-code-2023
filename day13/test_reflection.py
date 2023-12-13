import unittest

from day13.reflection import compute_reflections_number_from_file


class TestReflections(unittest.TestCase):

    def test_should_answer_example(self):
        self.assertEqual(405, compute_reflections_number_from_file('example'))

    def test_should_answer_input(self):
        self.assertEqual(30158, compute_reflections_number_from_file('input'))

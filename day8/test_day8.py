import unittest

from day8.day8p1 import count_steps_from_a_to_z
from day8.day8p2 import count_steps_from_a_to_z_as_ghost, read_path_and_graph


class TestDay8Part1(unittest.TestCase):

    def test_should_get_steps_for_example_1(self):
        self.assertEqual(2, count_steps_from_a_to_z('example1'))

    def test_should_get_steps_for_example_2(self):
        self.assertEqual(6, count_steps_from_a_to_z('example2'))

    def test_should_get_steps_for_input(self):
        self.assertEqual(23147, count_steps_from_a_to_z('input'))


class TestDay8Part2(unittest.TestCase):

    def test_should_get_steps_for_example_3(self):
        self.assertEqual(6, count_steps_from_a_to_z_as_ghost('example3'))

    def test_should_index_paths_for_example_3(self):
        path, graph = read_path_and_graph('example3')
        path_index = graph.path_index(path)
        self.assertEqual("by_node{"
                         "'11A': by_starting_offset{"
                         "0: {'endings': [11Z at 2], 'end_node': 11Z}, "
                         "1: {'endings': [], 'end_node': XXX}}, "
                         "'11B': by_starting_offset{"
                         "0: {'endings': [], 'end_node': XXX}, "
                         "1: {'endings': [11Z at 1], 'end_node': 11B}}, "
                         "'11Z': by_starting_offset{"
                         "0: {'endings': [11Z at 2], 'end_node': 11Z}, "
                         "1: {'endings': [], 'end_node': XXX}}, "
                         "'22A': by_starting_offset{"
                         "0: {'endings': [], 'end_node': 22C}, "
                         "1: {'endings': [], 'end_node': XXX}}, "
                         "'22B': by_starting_offset{"
                         "0: {'endings': [22Z at 2], 'end_node': 22Z}, "
                         "1: {'endings': [22Z at 2], 'end_node': 22Z}}, "
                         "'22C': by_starting_offset{"
                         "0: {'endings': [22Z at 1], 'end_node': 22B}, "
                         "1: {'endings': [22Z at 1], 'end_node': 22B}}, "
                         "'22Z': by_starting_offset{"
                         "0: {'endings': [], 'end_node': 22C}, "
                         "1: {'endings': [], 'end_node': 22C}}, "
                         "'XXX': by_starting_offset{"
                         "0: {'endings': [], 'end_node': XXX}, "
                         "1: {'endings': [], 'end_node': XXX}}}",
                         repr(path_index))

    def test_should_get_steps_for_input(self):
        self.assertEqual(0, count_steps_from_a_to_z_as_ghost('input'))

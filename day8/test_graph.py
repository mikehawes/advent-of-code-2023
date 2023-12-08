import unittest

from day8.day8p2 import read_path_and_graph
from day8.graph import NodePathState


class TestGraph(unittest.TestCase):

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

    def test_should_expand_paths_for_example_3(self):
        path, graph = read_path_and_graph('example3')
        path_index = graph.path_index(path, index_length=3)
        self.assertEqual("by_starting_offset{"
                         "0: {'endings': [11Z at 2], 'end_node': 11B}, "
                         "1: {'endings': [], 'end_node': XXX}}",
                         repr(path_index.indexes_by_node_number[0]))

    def test_should_find_next_state(self):
        path, graph = read_path_and_graph('input')
        path_index = graph.path_index(path, 1000)
        before = NodePathState(current_nodes=graph.nodes_by_labels(['JGL', 'LTN', 'QNN', 'GGT', 'NXT', 'DCF']),
                               steps=22000000000000,
                               path_offset=24)
        after_by_graph = graph.next_state(before, path, max_steps=1000)
        after_by_index = path_index.next_state(before)
        self.assertEqual(
            repr(NodePathState(current_nodes=graph.nodes_by_labels(['FDV', 'FKJ', 'VRL', 'NNL', 'GGX', 'RKP']),
                               steps=22000000001000,
                               path_offset=145,
                               iterations=1)),
            repr(after_by_graph))
        self.assertEqual(repr(after_by_graph), repr(after_by_index))

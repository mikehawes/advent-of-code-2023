import unittest

import networkx as nx
from approvaltests import verify

from day25.wires import read_nx_graph_from_file, find_product_of_split_group_sizes


class TestWires(unittest.TestCase):

    def test_should_split_example_into_two(self):
        graph = read_nx_graph_from_file('example')
        left, right = next(nx.community.girvan_newman(graph))
        verify('\n'.join([str(sorted(left)), str(sorted(right))]))

    def test_should_find_product_of_split_graph_sizes_for_example(self):
        graph = read_nx_graph_from_file('example')
        self.assertEqual(54, find_product_of_split_group_sizes(graph))

    def test_should_find_product_of_split_graph_sizes_for_input(self):
        graph = read_nx_graph_from_file('input')
        self.assertEqual(514786, find_product_of_split_group_sizes(graph))

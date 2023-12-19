import unittest

from approvaltests import verify

from day19.input import load_workflows_and_parts_from_file
from day19.workflows_printer import print_part_ranges


class TestWorkflows(unittest.TestCase):

    def test_should_find_accepted_parts_for_example(self):
        workflows, parts = load_workflows_and_parts_from_file('example')
        verify('\n'.join(map(str, workflows.list_accepted(parts))))

    def test_should_sum_accepted_parts_for_example(self):
        workflows, parts = load_workflows_and_parts_from_file('example')
        self.assertEqual(19114, workflows.sum_accepted_scores(parts))

    def test_should_sum_accepted_parts_for_input(self):
        workflows, parts = load_workflows_and_parts_from_file('input')
        self.assertEqual(362930, workflows.sum_accepted_scores(parts))

    def test_should_find_accepted_ranges_for_example(self):
        workflows, _ = load_workflows_and_parts_from_file('example')
        verify(print_part_ranges(workflows.find_accepted_ranges()))

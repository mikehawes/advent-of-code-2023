import unittest

from approvaltests import verify

from day19.input import load_workflows_and_parts_from_file


class TestWorkflows(unittest.TestCase):

    def test_should_find_accepted_parts_for_example(self):
        workflows, parts = load_workflows_and_parts_from_file('example')
        verify('\n'.join(map(str, workflows.list_accepted(parts))))

    def test_should_sum_accepted_parts_for_example(self):
        workflows, parts = load_workflows_and_parts_from_file('example')
        self.assertEqual(19114, workflows.sum_accepted_scores(parts))

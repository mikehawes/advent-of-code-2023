import unittest

from approvaltests import verify

from day19.input import read_workflows


class TestRules(unittest.TestCase):

    def test_should_filter_range_by_greater_than(self):
        workflows = read_workflows(['in{x>2662:A,R}'])
        verify(workflows.find_accepted_ranges())

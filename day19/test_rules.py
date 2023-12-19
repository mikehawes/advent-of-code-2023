import unittest

from approvaltests import verify

from day19.workflows_printer import print_workflow_ranges


class TestRules(unittest.TestCase):

    def test_should_filter_by_single_condition(self):
        verify(print_workflow_ranges([
            ['in{x>2662:A,R}'],
            ['in{x<2662:A,R}'],
            ['in{x>2662:R,A}'],
            ['in{x<2662:R,A}']
        ]))

    def test_should_include_else_condition(self):
        verify(print_workflow_ranges([
            ['in{x>2662:R,x>1000:A,R}'],
            ['in{x>2662:A,x<1000:A,R}'],
            ['in{x>2662:A,x>1000:A,R}']
        ]))

    def test_should_combine_workflows(self):
        verify(print_workflow_ranges([
            ['in{x>2662:then,R}',
             'then{x<3000:A,R}'],
        ]))

    def test_should_handle_different_attributes(self):
        verify(print_workflow_ranges([
            ['in{x>2662:then,x>1000:A,R}',
             'then{a<3000:A,R}'],
        ]))

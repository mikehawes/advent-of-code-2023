import io
import unittest

from approvaltests import verify

from day19.input import read_workflows


def print_workflow_ranges(workflows_cases):
    out = io.StringIO()
    for workflow_lines in workflows_cases:
        workflows = read_workflows(workflow_lines)
        print('Workflows:', file=out)
        for line in workflow_lines:
            print(line, file=out)
        print('Accepted ranges:', file=out)
        print(workflows.find_accepted_ranges(), file=out)
        print(file=out)
    return out.getvalue()


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

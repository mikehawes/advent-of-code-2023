import io

from day19.input import read_workflows


def print_workflow_ranges(workflows_cases):
    out = io.StringIO()
    for workflow_lines in workflows_cases:
        workflows = read_workflows(workflow_lines)
        print('Workflows:', file=out)
        for line in workflow_lines:
            print(line, file=out)
        print('Accepted ranges:', file=out)
        print(print_part_ranges(workflows.find_accepted_ranges()), file=out)
        print(file=out)
    return out.getvalue()


def print_part_ranges(part_ranges):
    return '\n'.join(map(str, part_ranges))

import re

from day19.steps import CompareAttribute, AcceptPart, RejectPart, GoToWorkflow, Workflow
from day19.workflows import Workflows, Part


def load_workflows_and_parts_from_file(input_file):
    workflows = {}
    parts = []
    with open(input_file, 'r') as file:
        for line in file:
            match = re.match(r'([a-z]+)\{(.+)}', line)
            if match:
                name = match.group(1)
                steps = match.group(2).split(',')
                workflows[name] = Workflow(read_steps(steps))
            else:
                break
        for line in file:
            match = re.match(r'\{(.+)}', line)
            if match:
                attributes = match.group(1).split(',')
                parts.append(read_part(attributes))
    return Workflows(workflows), parts


def read_steps(steps):
    return list(map(read_step, steps))


def read_step(step):
    comparison_match = re.match('([xmas])([<>])([0-9]+):(.+)', step)
    if comparison_match:
        return CompareAttribute(attribute=comparison_match.group(1),
                                test=comparison_match.group(2),
                                value=int(comparison_match.group(3)),
                                next_workflow=comparison_match.group(4))
    elif step == 'A':
        return AcceptPart()
    elif step == 'R':
        return RejectPart()
    else:
        return GoToWorkflow(step)


def read_part(attributes):
    score_by_attribute = dict(map(read_attribute_score, attributes))
    return Part(score_by_attribute)


def read_attribute_score(attribute):
    parts = attribute.split('=')
    return parts[0], int(parts[1])

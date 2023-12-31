import re

from day19.rules import CompareAttribute, AcceptPart, RejectPart, GoToWorkflow, Workflow
from day19.workflows import Workflows, Part


def load_workflows_and_parts_from_file(input_file):
    with open(input_file, 'r') as file:
        workflows = read_workflows(file)
        parts = read_parts(file)
    return workflows, parts


def read_workflows(lines):
    workflows = {}
    for line in lines:
        match = re.match(r'([a-z]+)\{(.+)}', line)
        if match:
            name = match.group(1)
            rules = match.group(2).split(',')
            workflows[name] = Workflow(read_rules(rules))
        else:
            break
    return Workflows(workflows)


def read_parts(lines):
    parts = []
    for line in lines:
        match = re.match(r'\{(.+)}', line)
        if match:
            attributes = match.group(1).split(',')
            parts.append(read_part(attributes))
        else:
            break
    return parts


def read_rules(rules):
    return list(map(read_rule, rules))


def read_rule(rule):
    comparison_match = re.match('([xmas])([<>])([0-9]+):(.+)', rule)
    if comparison_match:
        return CompareAttribute(attribute=comparison_match.group(1),
                                test=comparison_match.group(2),
                                value=int(comparison_match.group(3)),
                                next_workflow=comparison_match.group(4))
    elif rule == 'A':
        return AcceptPart()
    elif rule == 'R':
        return RejectPart()
    else:
        return GoToWorkflow(rule)


def read_part(attributes):
    score_by_attribute = dict(map(read_attribute_score, attributes))
    return Part(score_by_attribute)


def read_attribute_score(attribute):
    parts = attribute.split('=')
    return parts[0], int(parts[1])

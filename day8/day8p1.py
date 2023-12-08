import re


def count_steps(path, paths_by_node, start, end):
    steps = 0
    node = start
    while True:
        for direction in path:
            paths = paths_by_node[node]
            if direction == 'L':
                node = paths[0]
                steps += 1
            elif direction == 'R':
                node = paths[1]
                steps += 1
            if node == end:
                return steps


def count_steps_from_a_to_z(input_file):
    file = open(input_file, 'r')
    path = file.readline().strip()
    paths_by_node = {}
    for line in file:
        nodes = re.findall("[A-Z]+", line)
        if len(nodes) == 3:
            paths_by_node[nodes[0]] = (nodes[1], nodes[2])
    return count_steps(path, paths_by_node, 'AAA', 'ZZZ')


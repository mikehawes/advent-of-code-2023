import re
import time

from day8.graph import InitNode, Graph


def count_steps(path, graph):
    nodes = graph.start_nodes()
    print('Starting nodes:', nodes)
    start_time = time.time()
    steps = 0
    while True:
        for direction in path:
            next_nodes = graph.get_next_nodes(nodes, direction)
            steps += 1
            if all(map(lambda n: n.is_end, next_nodes)):
                return steps
            if steps % 100000000 == 0:
                now = time.time()
                print('Steps:', steps)
                print('Nodes:', nodes)
                print('Direction:', direction)
                print('Next nodes:', next_nodes)
                print('Seconds elapsed:', round(now - start_time, 2))
            nodes = next_nodes


def count_steps_from_a_to_z_as_ghost(input_file):
    init_nodes = []
    with open(input_file, 'r') as file:
        path = file.readline().strip()
        for line in file:
            nodes = re.findall("[A-Z0-9]+", line)
            if len(nodes) == 3:
                init_nodes.append(InitNode(nodes[0], nodes[1], nodes[2]))

    graph = Graph(init_nodes)

    print('{} directions:'.format(len(path)), path)
    print('{} nodes:'.format(graph.count()), graph)
    return count_steps(path, graph)


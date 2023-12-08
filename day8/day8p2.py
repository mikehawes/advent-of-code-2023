import re
import time

from day8.graph import InitNode, Graph


def count_steps(path, graph):
    nodes = graph.start_nodes()
    state = graph.start_state()
    path_index = graph.path_index(path)
    print('Starting nodes:', nodes)
    start_time = time.time()
    while True:
        next_state = path_index.next_state(state)
        if next_state.at_end:
            return next_state.steps
        if next_state.iterations % 100000000 == 0:
            now = time.time()
            print('Iterations:', next_state.iterations)
            print('Steps:', next_state.steps)
            print('Prev nodes:', state.current_nodes)
            print('Nodes:', next_state.current_nodes)
            print('Path offset:', next_state.path_offset)
            print('Seconds elapsed:', round(now - start_time, 2))
        state = next_state


def read_path_and_graph(input_file):
    init_nodes = []
    with open(input_file, 'r') as file:
        path = file.readline().strip()
        for line in file:
            nodes = re.findall("[A-Z0-9]+", line)
            if len(nodes) == 3:
                init_nodes.append(InitNode(nodes[0], nodes[1], nodes[2]))

    graph = Graph(init_nodes)
    return path, graph


def count_steps_from_a_to_z_as_ghost(input_file):
    path, graph = read_path_and_graph(input_file)

    print('{} directions:'.format(len(path)), path)
    print('{} nodes:'.format(graph.count()), graph)
    return count_steps(path, graph)

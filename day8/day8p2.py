import time

from day8.graph import read_path_and_graph


def count_steps(path, graph):
    nodes = graph.start_nodes()
    state = graph.start_state()
    print('Starting nodes:', nodes)
    path_index = graph.path_index(path, index_length=100000)
    print('Indexed paths')
    start_time = time.time()
    while True:
        next_state = path_index.next_state(state)
        if next_state.at_end:
            return next_state.steps
        if next_state.iterations % 10000000 == 0:
            now = time.time()
            print('Iterations:', next_state.iterations)
            print('Steps:', next_state.steps)
            print('Prev nodes:', state.current_nodes)
            print('Nodes:', next_state.current_nodes)
            print('Path offset:', next_state.path_offset)
            print('Seconds elapsed:', round(now - start_time, 2))
        state = next_state


def count_steps_from_a_to_z_as_ghost(input_file):
    path, graph = read_path_and_graph(input_file)

    print('{} directions:'.format(len(path)), path)
    print('{} nodes:'.format(graph.count()), graph)
    return count_steps(path, graph)

import datetime
import time

from day08.graph import read_path_and_graph


def count_steps(path, graph):
    nodes = graph.start_nodes()
    state = graph.start_state()
    print('Starting nodes:', nodes)
    path_index = graph.path_index(path, index_length=100000)
    start_time = time.time()
    while True:
        next_state = path_index.next_state(state)
        if next_state.at_end:
            print('Finished')
            print('Prev state:', state)
            print(' End state:', next_state)
            print('Time traversing states:', datetime.timedelta(seconds=time.time() - start_time))
            return next_state.rules
        if next_state.iterations % 10000000 == 0:
            print('Prev state:', state)
            print(' New state:', next_state)
            print('Time traversing states:', datetime.timedelta(seconds=time.time() - start_time))
        state = next_state


def count_steps_from_a_to_z_as_ghost(input_file):
    path, graph = read_path_and_graph(input_file)

    print('{} directions:'.format(len(path)), path)
    print('{} nodes:'.format(graph.count()), graph)
    return count_steps(path, graph)

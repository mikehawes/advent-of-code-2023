import networkx as nx


def read_nx_graph_from_file(input_file):
    graph = nx.Graph()
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.split(':')
            left = parts[0]
            connected = parts[1].strip().split(' ')
            for right in connected:
                graph.add_edge(left, right)
    return graph


def find_product_of_split_group_sizes(graph: nx.Graph):
    left, right = next(nx.community.girvan_newman(graph))
    return len(left) * len(right)

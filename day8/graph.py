import re


class Node:
    def __init__(self, init_node, number_by_label):
        self.label = init_node.label
        self.number = number_by_label[init_node.label]
        self.left_number = number_by_label[init_node.left_label]
        self.right_number = number_by_label[init_node.right_label]
        self.is_start = self.label.endswith('A')
        self.is_end = self.label.endswith('Z')

    def get_next_node(self, nodes, direction):
        if direction == 'L':
            return nodes[self.left_number]
        if direction == 'R':
            return nodes[self.right_number]

    def __repr__(self):
        return '{}'.format(self.label)


class InitNode:
    def __init__(self, label, left_label, right_label):
        self.label = label
        self.left_label = left_label
        self.right_label = right_label

    def __repr__(self):
        return '{} = ({}, {})'.format(self.label, self.left_label, self.right_label)


class NodePathState:
    def __init__(self, current_nodes, steps, path_offset, iterations=0, at_end=False):
        self.current_nodes = current_nodes
        self.steps = steps
        self.path_offset = path_offset
        self.iterations = iterations
        self.at_end = at_end

    def __repr__(self):
        return '{}'.format({
            'nodes': self.current_nodes,
            'steps': self.steps,
            'path_offset': self.path_offset,
            'iterations': self.iterations,
            'at_end': self.at_end
        })


class NodePathEnding:
    def __init__(self, end_node, num_steps):
        self.end_node = end_node
        self.num_steps = num_steps

    def __repr__(self):
        return '{} at {}'.format(self.end_node, self.num_steps)


class NodePathIndex:
    def __init__(self, node, nodes, path, index_length):
        self.endings_by_starting_offset = []
        self.end_node_by_starting_offset = []
        self.index_length = index_length
        self.path_len = len(path)
        for starting_offset in range(0, self.path_len):
            current_node = node
            endings = []
            for num_steps in range(1, index_length + 1):
                offset = starting_offset + num_steps - 1
                path_offset = offset % self.path_len
                direction = path[path_offset]
                current_node = current_node.get_next_node(nodes, direction)
                if current_node.is_end:
                    endings.append(NodePathEnding(current_node, num_steps))
            self.endings_by_starting_offset.append(endings)
            self.end_node_by_starting_offset.append(current_node)

    def __repr__(self):
        offsets = {}
        for i in range(0, self.path_len):
            offsets[i] = {
                'endings': self.endings_by_starting_offset[i],
                'end_node': self.end_node_by_starting_offset[i]
            }
        return 'by_starting_offset{}'.format(offsets)


class PathIndex:
    def __init__(self, nodes, path, index_length):
        self.nodes = nodes
        self.path = path
        self.path_len = len(path)
        self.index_length = index_length
        self.indexes_by_node_number = []
        for i, node in enumerate(nodes):
            print("Computing path index for node {}, {} of {}".format(node, i + 1, len(nodes)))
            self.indexes_by_node_number.append(NodePathIndex(node, nodes, path, index_length))

    def next_state(self, state):
        next_nodes = []
        end_nodes_by_offset = {}
        for node in state.current_nodes:
            node_index = self.indexes_by_node_number[node.number]
            for ending in node_index.endings_by_starting_offset[state.path_offset]:
                if ending.num_steps not in end_nodes_by_offset:
                    end_nodes_by_offset[ending.num_steps] = []
                end_nodes_by_offset[ending.num_steps].append(ending.end_node)
            next_nodes.append(node_index.end_node_by_starting_offset[state.path_offset])
        for offset, end_nodes in end_nodes_by_offset.items():
            if len(end_nodes) == len(state.current_nodes):
                end_path_offset = (state.path_offset + offset) % self.path_len
                return NodePathState(current_nodes=end_nodes, steps=state.steps + offset, path_offset=end_path_offset,
                                     iterations=state.iterations + 1, at_end=True)
        new_path_offset = (state.path_offset + self.index_length) % self.path_len
        return NodePathState(current_nodes=next_nodes, steps=state.steps + self.index_length,
                             path_offset=new_path_offset, iterations=state.iterations + 1)

    def __repr__(self):
        by_node = {}
        for i in range(0, len(self.nodes)):
            node = self.nodes[i]
            by_node[node.label] = self.indexes_by_node_number[i]
        return 'by_node{}'.format(by_node)


class Graph:
    def __init__(self, init_nodes):
        self.number_by_label = {}
        for i, init_node in enumerate(init_nodes):
            self.number_by_label[init_node.label] = i
        self.nodes = []
        for init_node in init_nodes:
            self.nodes.append(Node(init_node, self.number_by_label))

    def path_index(self, path, index_length=None):
        if not index_length:
            index_length = len(path)
        return PathIndex(self.nodes, path, index_length)

    def start_state(self):
        return NodePathState(current_nodes=self.start_nodes(), steps=0, path_offset=0)

    def next_state(self, state, path, max_steps):
        steps = state.steps
        nodes = state.current_nodes
        offset = state.path_offset
        stage_steps = 0
        while stage_steps < max_steps:
            nodes = self.next_nodes(nodes, path[offset % len(path)])
            stage_steps += 1
            offset += 1
            if all(map(lambda n: n.is_end, nodes)):
                return NodePathState(current_nodes=nodes, steps=steps + stage_steps, path_offset=offset % len(path),
                                     iterations=state.iterations + 1, at_end=True)
        return NodePathState(current_nodes=nodes, steps=steps + stage_steps, path_offset=offset % len(path),
                             iterations=state.iterations + 1)

    def next_nodes(self, nodes, direction):
        return list(map(lambda n: n.get_next_node(self.nodes, direction), nodes))

    def node_by_label(self, label):
        return self.nodes[self.number_by_label[label]]

    def nodes_by_labels(self, labels):
        return list(map(lambda label: self.node_by_label(label), labels))

    def start_nodes(self):
        return list(filter(lambda n: n.is_start, self.nodes))

    def count(self):
        return len(self.nodes)

    def __repr__(self):
        return '{}'.format(self.nodes)


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

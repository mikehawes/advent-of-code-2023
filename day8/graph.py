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


class NodePathEnding:
    def __init__(self, end_node, num_steps):
        self.end_node = end_node
        self.num_steps = num_steps

    def __repr__(self):
        return '{} at {}'.format(self.end_node, self.num_steps)


class NodePathIndex:
    def __init__(self, node, nodes, path):
        self.endings_by_starting_offset = []
        self.end_node_by_starting_offset = []
        self.path_len = len(path)
        for i in range(0, len(path)):
            current_node = node
            endings = []
            for num_steps in range(1, len(path) + 1):
                offset = i + num_steps - 1
                if offset >= len(path):
                    offset -= len(path)
                direction = path[offset]
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
    def __init__(self, nodes, path):
        self.nodes = nodes
        self.path = path
        self.indexes_by_node_number = []
        for node in nodes:
            self.indexes_by_node_number.append(NodePathIndex(node, nodes, path))

    def next_state(self, state):
        next_nodes = []
        end_nodes_by_offset = {}
        for node in state.current_nodes:
            node_index = self.indexes_by_node_number[node.number]
            endings = node_index.endings_by_starting_offset[state.path_offset]
            for ending in endings:
                if ending.num_steps not in end_nodes_by_offset:
                    end_nodes_by_offset[ending.num_steps] = []
                end_nodes_by_offset[ending.num_steps].append(ending.end_node)
            next_nodes.append(node_index.end_node_by_starting_offset[state.path_offset])
        for offset, nodes in end_nodes_by_offset.items():
            if len(nodes) == len(state.current_nodes):
                return NodePathState(current_nodes=nodes, steps=state.steps + offset, path_offset=offset,
                                     iterations=state.iterations + 1, at_end=True)
        return NodePathState(current_nodes=next_nodes, steps=state.steps + len(self.path),
                             path_offset=state.path_offset, iterations=state.iterations + 1)

    def __repr__(self):
        by_node = {}
        for i in range(0, len(self.nodes)):
            node = self.nodes[i]
            by_node[node.label] = self.indexes_by_node_number[i]
        return 'by_node{}'.format(by_node)


class Graph:
    def __init__(self, init_nodes):
        number_by_label = {}
        for i, init_node in enumerate(init_nodes):
            number_by_label[init_node.label] = i
        self.nodes = []
        for init_node in init_nodes:
            self.nodes.append(Node(init_node, number_by_label))

    def path_index(self, path):
        return PathIndex(self.nodes, path)

    def start_state(self):
        return NodePathState(current_nodes=self.start_nodes(), steps=0, path_offset=0)

    def start_nodes(self):
        return list(filter(lambda n: n.is_start, self.nodes))

    def count(self):
        return len(self.nodes)

    def __repr__(self):
        return '{}'.format(self.nodes)

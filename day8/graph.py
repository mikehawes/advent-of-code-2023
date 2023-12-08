class Node:
    def __init__(self, init_node, number_by_label):
        self.label = init_node.label
        self.number = number_by_label[init_node.label]
        self.left_number = number_by_label[init_node.left_label]
        self.right_number = number_by_label[init_node.right_label]
        self.is_start = self.label.endswith('A')
        self.is_end = self.label.endswith('Z')

    def __repr__(self):
        return '{}'.format(self.label)


class InitNode:
    def __init__(self, label, left_label, right_label):
        self.label = label
        self.left_label = left_label
        self.right_label = right_label

    def __repr__(self):
        return '{} = ({}, {})'.format(self.label, self.left_label, self.right_label)


class Graph:
    def __init__(self, init_nodes):
        number_by_label = {}
        for i, init_node in enumerate(init_nodes):
            number_by_label[init_node.label] = i
        self.nodes = []
        for init_node in init_nodes:
            self.nodes.append(Node(init_node, number_by_label))

    def start_nodes(self):
        return list(filter(lambda n: n.is_start, self.nodes))

    def get_next_nodes(self, nodes, direction):
        return list(map(lambda n: self.get_next_node(n, direction), nodes))

    def get_next_node(self, node, direction):
        if direction == 'L':
            return self.nodes[node.left_number]
        if direction == 'R':
            return self.nodes[node.right_number]

    def count(self):
        return len(self.nodes)

    def __repr__(self):
        return '{}'.format(self.nodes)

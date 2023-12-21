import matplotlib.pyplot as plt
import networkx as nx

from day20.input import read_module_circuit_from_file
from day20.modules import ConjunctionModule, FlipFlopModule
from day20.pulses_printer import print_module_label, print_module_label_with_inputs, print_sent


class CircuitGraph:
    def __init__(self, circuit, include_state=False):
        self.circuit = circuit
        self.graph = nx.DiGraph()
        self.labels = {}
        self.conjunctions = []
        self.flip_flops = []
        self.others = []
        for module in circuit.module_by_name.values():
            if include_state:
                label = print_module_label_with_inputs(module)
            else:
                label = print_module_label(module)
            self.labels[module.name] = label
            if isinstance(module, ConjunctionModule):
                self.conjunctions.append(module.name)
            elif isinstance(module, FlipFlopModule):
                self.flip_flops.append(module.name)
            else:
                self.others.append(module.name)
            self.graph.add_node(module.name, object=module)
            for module_output in module.outputs:
                self.graph.add_edge(module.name, module_output)

    def render(self, figure_num=1, file=None):
        plt.figure(figure_num, (20, 12))
        pos = nx.nx_agraph.graphviz_layout(self.graph, prog='neato')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.conjunctions, node_color='yellow')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.flip_flops, node_color='orange')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.others, node_color='grey')
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos, self.labels)
        plt.axis('off')
        if file:
            plt.savefig(file)
        plt.show()


graph = read_module_circuit_from_file('input')
subgraph = graph.split_by_output_at_module('broadcaster')[2]

subgraph.press_button_times(3584)
CircuitGraph(subgraph, include_state=True).render()
subgraph.press_button_times(176)
CircuitGraph(subgraph, include_state=True).render()
sent = subgraph.press_button()
print(print_sent(sent))

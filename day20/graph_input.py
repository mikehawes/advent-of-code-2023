import matplotlib.pyplot as plt
import networkx as nx

from day20.input import read_module_circuit_from_file
from day20.modules import ConjunctionModule, FlipFlopModule
from day20.pulses_printer import print_module_label, print_modules

circuit = read_module_circuit_from_file('input')

graph = nx.DiGraph()
labels = {}
conjunctions = []
flip_flops = []
others = []
for module in circuit.module_by_name.values():
    labels[module.name] = print_module_label(module)
    if isinstance(module, ConjunctionModule):
        conjunctions.append(module.name)
    elif isinstance(module, FlipFlopModule):
        flip_flops.append(module.name)
    else:
        others.append(module.name)
    graph.add_node(module.name, object=module)
    for module_output in module.outputs:
        graph.add_edge(module.name, module_output)

plt.figure(1, (20, 12))
pos = nx.nx_agraph.graphviz_layout(graph, prog='neato')
nx.draw_networkx_nodes(graph, pos, nodelist=conjunctions, node_color='yellow')
nx.draw_networkx_nodes(graph, pos, nodelist=flip_flops, node_color='orange')
nx.draw_networkx_nodes(graph, pos, nodelist=others, node_color='grey')
nx.draw_networkx_edges(graph, pos)
nx.draw_networkx_labels(graph, pos, labels)
print(graph)
print(print_modules(circuit.sort_modules_with_root('rx')))
plt.axis('off')
plt.savefig('graph.pdf')
plt.show()

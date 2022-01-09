import networkx as nx 
import matplotlib.pyplot as plt 
import dwave_networkx as dnx 
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
s5=nx.star_graph(3)
G=nx.Graph()
G.add_nodes_from(["1","2","3","4"])
G.add_edge("1","2")
nx.draw(G, with_labels=True)
plt.savefig('grafo1,2')
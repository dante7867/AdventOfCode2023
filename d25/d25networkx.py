"""
https://adventofcode.com/2023/day/25
"""

import networkx as nx


G = nx.Graph()

with open('in.txt', 'r') as f: 
    for line in f.readlines():
        line = line.strip()
        key, vals = line.split(':')
        key = key.strip('')
        vals = [v.strip() for v in vals[1:].split()]
        for nb in vals:
            G.add_edge(key, nb,capacity=1.0)
            
nodes = list(G.nodes)
for n1, n2 in zip(nodes, nodes[1:]):
    cut_value, partition = nx.minimum_cut(G, n1, n2)
    reachable, non_reachable = partition
    if len(reachable) > 1 and len(non_reachable) > 1:
        print('p2:', len(reachable)*len(non_reachable)) 
        break
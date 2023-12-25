"""
https://adventofcode.com/2023/day/25
"""

from math import comb
from copy import deepcopy
from collections import defaultdict
from itertools import combinations


CONNECTIONS = {}
with open('ex.txt', 'r') as f: 
    for line in f.readlines():
        line = line.strip()
        key, vals = line.split(':')
        key = key.strip('')
        vals = [v.strip() for v in vals[1:].split()]
        CONNECTIONS[key] = vals


graph = defaultdict(set)
for comp, conns in CONNECTIONS.items():
    for conn in conns:
        graph[comp].add(conn)
        graph[conn].add(comp)

NUM_OF_ALL_NODES = len(graph)

list_of_interesting_conenctions = set()
for con1 in CONNECTIONS:
    for con2 in CONNECTIONS[con1]:
        list_of_interesting_conenctions.add(tuple(sorted([con1, con2])))

print(f"{len(list_of_interesting_conenctions)=}")


def get_connected(node):
    global graph
    nodes_to_check = [node]
    seen = set()
    while nodes_to_check:
        current = nodes_to_check.pop()
        seen.add(current)
        if current in graph:
            for connected in graph[current]:
                if connected not in seen:
                    nodes_to_check.append(connected)
    return seen   


def count_groups(pairs):
    global graph
    graph = disconnect(pairs)
    components = list(CONNECTIONS)
    ans = 0
    
    group_lens = []
    node1, node2 = pairs[0]

    if len(get_connected(node1)) == NUM_OF_ALL_NODES:
        ans = -1
    else:
        l1 = len(get_connected(node1))
        l2 = len(get_connected(node2))
        ans = l1 * l2

    graph = reconnect(pairs)

    return ans


def disconnect(pairs):
    for pair in pairs:
        p1, p2 = pair
        if p1 in graph:
            graph[p1].remove(p2)

        if p2 in graph:
            graph[p2].remove(p1)
    return graph


def reconnect(pairs):
    for pair in pairs:
        p1, p2 = pair
        if p1 in graph:
            graph[p1].add(p2)

        if p2 in graph:
            graph[p2].add(p1)
    return graph

# print('p1:', count_groups(components, disconnections=[]))
# print('p1:', count_groups(disconnections=[('hfx','pzl'),('bvb', 'cmg'),('nvd','jqt')]))



def part1():
    num_of_all_combinations = f"{comb(len(list_of_interesting_conenctions), 3)}"
    print(num_of_all_combinations)
    three_pairs = combinations(list_of_interesting_conenctions, 3)

    i=0
    for tp in three_pairs:
        i+=1
        print(f"{i}/{num_of_all_combinations}")
        check = count_groups(tp)
        if check != -1:
            return check

print('p1:', part1())


def get_all_possible_paths(start, end):
    global graph
    finished_ways = []
    ways = [( (start,))]
    while ways:
        way = ways.pop()
        if end == way[-1]:
            print(way)
            finished_ways.append(way)
        else:
            last = way[-1]
            neighbours = graph[last]
            for nxt in neighbours:
                if nxt not in way:
                    ways.append( way+(nxt,) )

# get_paths('qrt', 'klc')

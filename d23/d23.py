"""
https://adventofcode.com/2023/day/23
"""


from copy import deepcopy
from collections import defaultdict


with open('in.txt', 'r') as f: 
    M = [l.strip() for l in f.readlines()]

NEIGHTBOURS = defaultdict(set)
for y in range(len(M)):
    for x in range(len(M[0])):
        if y==0 and M[y][x] == '.':
            sy, sx = y, x
        if y==len(M)-1 and M[y][x] == '.':
            ey, ex = y, x
        if M[y][x] in '.><^v':
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                if 0<=y+dy<len(M) and 0<=x+dx<len(M[0]):
                    if M[y+dy][x+dx] in '.><^v':
                        NEIGHTBOURS[(y,x)].add((y+dy, x+dx))


SLOPES = {
    '>': (0,1),
    '<': (0,-1),
    '^': (-1,0),
    'v': (1, 0)
}


def brute_force_longest_way(sy, sx):
    stack = [(0, sy, sx, set())]
    ways = []

    while stack:
        s, y, x, seen = stack.pop()
        if y==ey and x==ex:
            ways.append(s)

        s += 1
        seen.add((y, x))

        if M[y][x] == '.':
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                if (y+dy, x+dx) not in seen:
                    if 0<=y+dy<len(M) and 0<=x+dx<len(M[0]):
                        if M[y+dy][x+dx] != '#':
                            stack.append((s, y+dy, x+dx, deepcopy(seen)))
        elif M[y][x] in '<>v^':
            dy, dx = SLOPES[M[y][x]]
            if (y+dy, x+dx) not in seen:
                if 0<=y+dy<len(M) and 0<=x+dx<len(M[0]):
                    if M[y+dy][x+dx] != '#':
                        stack.append((s, y+dy, x+dx, deepcopy(seen)))

    # print('ways:', ways)

    return max(ways)
        

print('p1:', brute_force_longest_way(sy, sx))

# seems like its to slow due to a lot of deepcopies
# cause it's really close to dfs executing withing 20ish seconds
def count_longest_path_to_slow(sy, sx, nodes):
    pos = [(0, sy, sx, [])]
    LENS = []
    while pos:
        s, y, x, seen = pos.pop()
        seen.append((y, x))
        if y==ey and x==ex:
            LENS.append(s)
        for npt, dist in nodes[(y,x)]:
            ny, nx = npt
            if (ny, nx) not in seen:
                pos.append((s + dist, ny, nx, deepcopy(seen)))
    print('LENS:', LENS)
    return max(LENS)


def get_last(nodes, cur, prev, dist):
    if len(nodes[cur]) != 2:
        return cur, dist
    else:
        for con in nodes[cur]:
            if con != prev:
                dist += abs(con[0]-cur[0]) + abs(con[1]-cur[1])
                return get_last(nodes, con, cur, dist)



def edge_contraction(sy, sx, nodes):
    new_nodes = defaultdict(set)

    stack = [(sy, sx)]
    seen = set()
    seen.add((sy, sx))

    while stack:
        node = stack.pop(0)
        seen.add(node)
        connections = nodes[node]
        for con in connections:
            dist = abs(con[0] - node[0]) + abs(con[1] - node[1])
            last, dist = get_last(nodes, con, node, dist)
            new_nodes[node].add((last, dist))
            if last not in seen:
                stack.append(last)
    return new_nodes

def dfs(y, x):
    global seen
    if (y, x) == (ey, ex):
        return 0

    maxi = -10**9
    seen.add((y, x))

    for pt, dist in graph[(y, x)]:
        ny, nx = pt
        if (ny, nx) not in seen:
            maxi = max(maxi, dfs(ny, nx) + dist)
    seen.remove((y,x))

    return maxi
        

graph = edge_contraction(sy, sx, NEIGHTBOURS)
seen = set()
# print('number of points in graph:', len(graph))
print('p2:', dfs(sy, sx))

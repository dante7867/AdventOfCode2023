"""
https://adventofcode.com/2023/day/17
"""

from sys import maxsize
import heapq


MOVES = {
    '>': (0, 1),
    '<': (0,-1),
    '^': (-1,0),
    'v': (1, 0)
}

BACK = {
    '>': '<',
    '<': '>',
    '^': 'v',
    'v': '^',
    '?': '?'
}


def get_possible_moves(last):
    LIMIT = 3
    possible_moves = []
    for mv in MOVES:
        if LIMIT != last.count(mv): # can't move same direction 3 times in a row
            if mv != BACK[last[-1]]: # can't turn 180 degrees
                possible_moves.append(mv)
    return possible_moves


def get_possible_moves_ultra(last):
    LOWER_LIMIT = 4
    UPPER_LIMIT = 10

    if not all(map(lambda x: x==last[-1], last[-LOWER_LIMIT])):
        return [last[-1]]

    possible_moves = []
    for mv in MOVES:
        if UPPER_LIMIT != last.count(mv):
            if mv != BACK[last[-1]]:
                possible_moves.append(mv)
    return possible_moves


def solve_with_dijkstra(sy, sx, limit, function_returning_movemenet_possibilites):
    pq = [(0, sy, sx, '?'*limit)]
    lowest = {}
    lowest[(sy,sx,'?'*limit)]=0
    while pq:
        c = heapq.heappop(pq)
        e, y, x, l3 = c
        if e > lowest[(y,x,l3)]:
            continue

        possible_moves = function_returning_movemenet_possibilites(l3)

        for pm in possible_moves:
            dy, dx = MOVES[pm]
            ny = y + dy
            nx = x + dx
            nl3 = l3[1:] + pm
            if 0<=ny<len(M) and 0<=nx<len(M[0]):
                ne = e + int(M[ny][nx])
                if (ny, nx, nl3) not in lowest:
                    lowest[(ny, nx, nl3)] = ne
                    heapq.heappush(pq,(ne, ny, nx, nl3))
                elif lowest[(ny, nx, nl3)] > ne:
                    lowest[(ny, nx, nl3)] = ne
                    heapq.heappush(pq,(ne, ny, nx, nl3))

    mini = maxsize
    for p, l in lowest.items():
        if p[0]==ey and p[1] == ex:
            mini = min(mini, l)

    return mini


with open('in.txt', 'r') as f:
    M = [l.strip() for l in f.readlines()]

sy, sx = 0, 0
ey, ex = len(M)-1, len(M[0])-1

print('p1:', solve_with_dijkstra(sy, sx, 3, get_possible_moves))
print('p2:', solve_with_dijkstra(sy, sx, 10, get_possible_moves_ultra))

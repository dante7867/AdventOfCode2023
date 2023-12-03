"""
https://adventofcode.com/2023/day/3
"""
from collections import Counter


with open('in.txt', 'r') as f: m = [l.strip() for l in f.readlines()]

symbols = []
for row in m:
    for ch in row:
        if not (ch.isdigit() or ch == '.'):
            symbols.append(ch)


def has_adjacent(y,x,m):
    adjacent_symbols = set()
    ans = False
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if not dx == dy == 0 :
                ny = y + dy
                nx = x + dx
                if ny > -1 and nx > -1 and ny < len(m) and nx < len(m[0]):
                    if m[ny][nx] in symbols:
                        adjacent_symbols.add((ny,nx))
    return adjacent_symbols


parts = []
adj = set()
sym2adjNumbers = {}
for y in range(len(m)):
    sNum = ''
    for x in range(len(m[0])):
        adjs = has_adjacent(y, x, m)

        if m[y][x].isdigit():
            sNum = sNum + m[y][x]
            for a in adjs:
                adj.add(a)

        if m[y][x].isdigit() == False or x==len(m[0])-1:
            if len(adj):
                parts.append(int(sNum))
            for a in adj:
                if a not in sym2adjNumbers:
                    sym2adjNumbers[a] = [int(sNum)]
                else:
                    sym2adjNumbers[a].append(int(sNum))
            sNum = ''
            adj = set()


p2 = 0
for k, v in sym2adjNumbers.items():
    if len(v) == 2 and m[k[0]][k[1]] == '*':
        p2 += v[0] * v[1]

print('p1:', sum(parts))
print('p2:', p2)

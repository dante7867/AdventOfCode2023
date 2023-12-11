"""
https://adventofcode.com/2023/day/11
"""

import sys


def find_rows_without_galaxies(m):
    no_galaxy_rows = []
    for i, row in enumerate(m):
        if not '#' in row:
            no_galaxy_rows.append(i)
    return no_galaxy_rows


def find_cols_without_galaxies(m):
    no_galaxy_cols = []
    for x in range(len(m[0])):
        found = False
        for y in range(len(m)):
            if m[y][x] == '#':
                found = True
                break
        if not found:
            no_galaxy_cols.append(x)
    return no_galaxy_cols


def expand(m):
    for r in no_galaxy_rows[::-1]:
        m = m[:r] + [m[r]] + m[r:]
    for c in no_galaxy_cols[::-1]:
        for i, r in enumerate(m):
            m[i] = m[i][:c] + '.' + m[i][c:]
    return m


def find_galaxies(m):
    galaxies = []
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == '#':
                galaxies.append((y,x))
    return galaxies


def count_dinstance(galaxies, D, no_galaxy_rows, no_galaxy_cols):
    shortest_sum = 0
    for cg in galaxies:
        for g in galaxies:
            dist = 0
            if cg != g:
                dist =  abs(cg[0]-g[0]) + abs(cg[1]-g[1])
                # 
                for y in range(min(cg[0], g[0]), max(cg[0],g[0])):
                    if y in no_galaxy_rows:
                        dist += D-1
                for x in range(min(cg[1], g[1]), max(cg[1],g[1])):
                    if x in no_galaxy_cols:
                        dist += D-1
            shortest_sum += dist
    return shortest_sum // 2


with open('in.txt', 'r') as f: 
    m = [l.strip() for l in f.readlines()]

no_galaxy_rows = find_rows_without_galaxies(m)
no_galaxy_cols = find_cols_without_galaxies(m)

galaxies = find_galaxies(m)

print('p1:', count_dinstance(galaxies, 2, no_galaxy_rows, no_galaxy_cols))
print('p2:', count_dinstance(galaxies, 1000000, no_galaxy_rows, no_galaxy_cols))

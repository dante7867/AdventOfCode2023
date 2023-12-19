"""
https://adventofcode.com/2023/day/18
"""

import re


with open('in.txt', 'r') as f: 
    lines = [l.strip() for l in f.readlines()]


pattern = r"^(\w)\s(\d+)\s\(#([a-z0-9]+)\)$"

# 0 means R, 1 means D, 2 means L, and 3 means U
N2D = {
    '0': "R",
    '1': "D",
    '2': "L",
    '3': "U"
}

ins_p1, ins_p2 = [], []
for line in lines:
    m = re.search(pattern, line)
    di, move, color = m.groups()[0], m.groups()[1], m.groups()[2]
    ins_p1.append((di, int(move), color))
    ins_p2.append((N2D[color[-1]], int('0x'+color[:5], 16), color))

D2V = {
    "U": (-1,0),
    "D": (1,0),
    "L": (0,-1),
    "R": (0,1)
}


def solve(ins):
    y, x = 0, 0
    vs = []
    points = []
    for di, val, _ in ins:
        st = (y,x)
        dy, dx = D2V[di]
        ey = y + dy * val
        ex = x + dx * val
        ed = (ey, ex)
        vs.append(sorted([(y, x), (ey, ex)]))
        y = ey
        x = ex
        points.append((y, x))

    boundry=0
    
    for v in vs:
        vsy, vsx = v[0]
        vey, vex = v[1]
        x_length = max(vex, vsx)-min(vex,vsx)
        y_length = max(vey, vsy)-min(vey,vsy)
        boundry += x_length + y_length


    # shoelance formula
    two_area = 0
    for p1, p2 in zip(points, points[1:]+points[0:1]):
        y1,x1 = p1
        y2,x2 = p2
        two_area += x1*y2-y1*x2

    area = abs(two_area//2)

    # pick's theorem 
    # area = interior + boundry/2 - 1
    # interior = area - boundry/2 + 1
    interior = area + boundry//2 + 1

    return interior


print('p1:', solve(ins_p1))
print('p2:', solve(ins_p2))

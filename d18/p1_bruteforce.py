"""
https://adventofcode.com/2023/day/18
"""

import re, sys


with open('in.txt', 'r') as f: 
    lines = [l.strip() for l in f.readlines()]


pattern = r"^(\w)\s(\d+)\s\(#([a-z0-9]+)\)$"

ins = []
for line in lines:
    m = re.search(pattern, line)
    di, move, color = m.groups()[0], m.groups()[1], m.groups()[2]
    ins.append((di, int(move), color))

# check boundries of map
x_mini, x_maxi = sys.maxsize, -sys.maxsize
y_mini, y_maxi = sys.maxsize, -sys.maxsize
y, x = 0, 0
for di, move, color in ins:
    if di == 'L':
        x -= move
    elif di == 'R':
        x += move
    elif di == 'U':
        y -= move
    elif di == 'D':
        y += move
    x_mini = min(x_mini, x)
    x_maxi = max(x_maxi, x)
    y_mini = min(y_mini, y)
    y_maxi = max(y_maxi, y)

print(f"{x_mini=}, {x_maxi=}")
print(f"{y_mini=}, {y_maxi=}")

M = []
for y in range(y_mini, y_maxi+1+2):
    R = []
    for x in range(x_mini, x_maxi+1+2):
        R.append('.')
    M.append(R)

def pm(M):
    for r in M:
        print(''.join(r))
    print()


y = -y_mini+1
x = -x_mini+1
M[y][x] = '#'
        

D2V = {
    "U": (-1,0),
    "D": (1,0),
    "L": (0,-1),
    "R": (0,1)
}


for di, move, color in ins:
    dy, dx = D2V[di]
    for _ in range(move):
        if 0<=y+dy<len(M) and 0<=x+dx<len(M[0]):
            y += dy
            x += dx
            M[y][x] = '#'
        else:
            break

pm(M)

M[0][0] = 'o'
outer = [(0,0)]
while outer:
    c = outer.pop()
    y, x = c

    M[y][x] = 'o'
    for dy in [-1,0,1]:
        for dx in [-1,0,1]:
            if not dy==dx==0:
                if 0<=y+dy<len(M) and 0<=x+dx<len(M[0]):
                    if M[y+dy][x+dx] == '.':
                        outer.append((y+dy, x+dx))

cnt = 0
for r in M:
    row_cnt = 0
    for ch in r:
        if ch != 'o':
            row_cnt += 1
    cnt += row_cnt
print('p1:', cnt)

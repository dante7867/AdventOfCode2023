"""
https://adventofcode.com/2023/day/16
"""


def move(M, y, x, dy, dx):
    ny = y + dy
    nx = x + dx
    if 0<=ny<len(M) and 0<=nx<len(M[0]):
        match M[ny][nx]:
            case '.':
                return [(ny, nx, dy, dx)]
            case '|':
                if (dy, dx) in [(-1,0), (1, 0)]: # ^ v
                    return [(ny, nx, dy, dx)]
                else: # < >
                    return [(ny, nx, -1, 0), (ny, nx, 1, 0)]
            case '-':
                if (dy, dx) in [(0,-1),(0,1)]: # < >
                    return [(ny, nx, dy, dx)]
                else: # ^ v
                    return [(ny, nx, 0, -1), (ny, nx, 0, 1)]
            case '/':
                if (dy, dx) == (0, 1): # > ... ^
                    return [(ny, nx, -1, 0)]
                elif (dy, dx) == (0, -1): # < ... v
                    return [(ny, nx, 1, 0)]
                elif (dy, dx) == (1, 0): # v ... <
                    return [(ny, nx, 0, -1)]
                elif (dy, dx) == (-1, 0): # ^ ... >
                    return [(ny, nx, 0, 1)]
            case '\\':
                if (dy, dx) == (0, 1): # > ... v
                    return [(ny, nx, 1, 0)]
                elif (dy, dx) == (0, -1): # < ... ^
                    return [(ny, nx, -1, 0)]
                elif (dy, dx) == (1, 0): # v ... >
                    return [(ny, nx, 0, 1)]
                elif (dy, dx) == (-1, 0): # ^ ... <
                    return [(ny, nx, 0, -1)]
    else: # out of map
        return [] 


def count_energized(sy, sx, sdy, sdx): 
    start = (sy, sx,sdy,sdx)
    hist = set()

    current = [start]
    while current:
        c = current.pop()
        y, x, dy, dx = c
        post_move = move(M, y, x, dy, dx)
        for ny, nx, dy, dx in post_move:
            if (ny, nx, dy, dx) not in hist:
                current.append((ny, nx, dy, dx))
                hist.add((ny, nx, dy, dx))

    return len(set((y,x) for y, x, a, b in hist))


with open('in.txt', 'r') as f: 
    M = [l.strip() for l in f.readlines()]

# P1
sy, sx = 0, -1
sdy, sdx = 0, 1
print('p1:', count_energized(sy, sx, sdy, sdx))

# P2
maxi = 0

# upper edge
sy = -1
for sx in range(len(M[0])):
    maxi = max(maxi, count_energized(sy, sx, 1, 0))

# lower edge
sy = len(M)
for sx in range(len(M[0])):
    maxi = max(maxi, count_energized(sy, sx, -1, 0))

# left edge
sx = -1
for sy in range(len(M)):
    maxi = max(maxi, count_energized(sy, sx, 0, 1))

# right edge
sx = len(M[0])
for sy in range(len(M)):
    maxi = max(maxi, count_energized(sy, sx, 0, -1))

print('p2:', maxi)

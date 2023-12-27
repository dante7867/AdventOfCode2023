"""
https://adventofcode.com/2023/day/21
"""

from collections import defaultdict

with open('in.txt', 'r') as f:
    M = [list(l.strip()) for l in f.readlines()]


def pm(M):
    for r in M:
        print(''.join(r))
    print()
    
sy, sx = -1, -1
for y in range(len(M)):
    for x in range(len(M[0])):
        if M[y][x] == 'S':
            sy, sx = y, x
        
assert sy>-1 and sx>-1


def solve_p1(y, x, max_steps):
    step = 0
    locs = set()
    locs.add((y, x))
    while step != max_steps:
        step += 1
        # print(f"{step=}")
        new_locs = set()
        while locs:
            y, x = locs.pop()
            for dy, dx in ((-1,0), (1,0), (0,1), (0,-1)):
                if 0<=y+dy<len(M) and 0<=x+dx<len(M[0]):
                    if M[y+dy][x+dx] != '#':
                        new_locs.add((y+dy, x+dx))
        locs = new_locs
    return len(locs)


print('p1:', solve_p1(sy, sx, 64))


def solve_p2(y, x, max_steps):
    GS = defaultdict(set)
    step = 0
    locs = set()
    locs.add((y, x))
    GS[(0, 0)] = locs
    while step != max_steps:
        step += 1
        new_locs = set()
        NGS = defaultdict(set)

        for G, locs in GS.items():
            while locs:
                y, x = locs.pop()
                for dy, dx in ((-1,0), (1,0), (0,1), (0,-1)):
                    gy, gx = G
                    ny = y+dy
                    nx = x+dx
                    if ny == -1:
                        gy -= 1
                        ny = len(M) - 1
                    elif ny == len(M):
                        gy += 1
                        ny = 0
                    elif nx == -1:
                        gx -= 1
                        nx = len(M[0]) - 1
                    elif nx == len(M[0]):
                        gx += 1
                        nx = 0
                    
                    if M[ny][nx] != '#':
                        NGS[(gy,gx)].add((ny, nx))
        GS = NGS

    return sum(len(s) for s in GS.values())


MAX_STEPS = 26501365
dim = len(M)

at_first_border = solve_p2(sy, sx, dim//2)
at_second_border =solve_p2(sy, sx, dim+dim//2)
at_third_border =solve_p2(sy, sx, dim+dim+dim//2)


# thanks for hints reddit
step = dim
finished = at_second_border - at_first_border 
rest = at_third_border-at_second_border
difference = rest - finished
possibilites_cnt = at_second_border

while step != MAX_STEPS-dim//2:
    step += dim
    possibilites_cnt += rest
    rest += difference

print('p2:', possibilites_cnt)

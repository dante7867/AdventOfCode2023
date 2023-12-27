"""
https://adventofcode.com/2023/day/21
"""


file_name = 'in.txt'
with open(file_name, 'r') as f:
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
# print(f"start: {sy=}, {sx=}")

cache = {}
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

def corners(y, x, max_steps):
    step = 0
    locs = set()
    locs.add((y, x, 0))
    while step != max_steps:
        step += 1
        # print(f"{step=}")
        new_locs = set()
        while locs:
            y, x = locs.pop()
            for dy, dx in ((-1,0), (1,0), (0,1), (0,-1)):
                if 0<=y+dy<len(M) and 0<=x+dx<len(M[0]):
                    if M[y+dy][x+dx] != '#':
                        new_locs.add((y+dy, x+dx, step))
        locs = new_locs
    locs = set([(y, x) for x, y, s in locs if s > 65])
    return locs


from collections import defaultdict, Counter


if file_name == 'in.txt':
# my 7730 <-> 7697
    BIG1 = 7730
    BIG2 = 7697
else:
# ex 42 <-> 39
    BIG1 = 42
    BIG2 = 39

def solve_p2(y, x, max_steps, XS):
    MOVE_CACHE = defaultdict(set)
    ret = []
    c = Counter()
    LOOPED = set()
    c[BIG1] = 0
    c[BIG2] = 0
    GS = defaultdict(set)
    step = 0
    locs = []
    locs.append((y, x))
    GS[(0, 0)] = locs
    LOCATIONS_CACHE = {}
    while step != max_steps:
        # print(step)
        # print(f"{step=}, {len(GS)=}")
        # unique_gardens = set()
        # for garden in GS.values():
        #     stiffed = tuple(sorted(list(garden)))
        #     unique_gardens.add(stiffed)
        # print(f"{len(unique_gardens)=}")
        step += 1
        NGS = defaultdict(set)
        for G, locs in GS.items():
            immutable_sorted_locs = tuple(sorted(list(locs)))
            gy, gx = G
            if immutable_sorted_locs in LOCATIONS_CACHE:
                NEIGHTBOUR_GARDENS = LOCATIONS_CACHE[immutable_sorted_locs]
            else:
                NEIGHTBOUR_GARDENS = defaultdict(set)
                for loc in immutable_sorted_locs:
                    y, x = loc
                    if (y, x) in MOVE_CACHE:
                        for ny, nx, dgy, dgx in MOVE_CACHE[(y, x)]:
                            NEIGHTBOUR_GARDENS[(dgy, dgx)].add((ny, nx))
                            #NGS[(gy+dgy, gx+dgx)].add((ny,nx))
                    else:
                        for dy, dx in ((-1,0), (1,0), (0,1), (0,-1)):
                            dgy, dgx = 0, 0
                            
                            ny = y+dy
                            nx = x+dx
                            
                            if ny == -1:
                                dgy = -1
                                ny = len(M) - 1
                            elif ny == len(M):
                                dgy = + 1
                                ny = 0
                            elif nx == -1:
                                dgx = -1
                                nx = len(M[0]) - 1
                            elif nx == len(M[0]):
                                dgx = 1
                                nx = 0
                            
                            if M[ny][nx] != '#':
                                # NGS[(gy+dgy,gx+dgx)].add((ny, nx))
                                NEIGHTBOUR_GARDENS[(dgy, dgx)].add((ny, nx))
                                MOVE_CACHE[(y,x)].add((ny, nx, dgy, dgx))
                LOCATIONS_CACHE[immutable_sorted_locs] = NEIGHTBOUR_GARDENS
            for dir_difs, pts in NEIGHTBOUR_GARDENS.items():
                dgy, dgx = dir_difs
                NGS[(gy+dgy,gx+dgx)].update(pts)
            
        GS.clear()
        c[BIG1], c[BIG2] = c[BIG2], c[BIG1]
        for k, v in NGS.items():
            if len(v)==BIG1:
                c[BIG1]+= 1
                LOOPED.add(k)
            elif k not in LOOPED:
                GS[k] = v
        # print(f"---{step}--- {len(LOOPED)=} , {len(GS)=}")
        # for G, s in GS.items():
            # print(f"key: {G} ->", len(s), sorted(list(s)))
        if step in XS:
            print('    ', step, 'all', sum(len(s) for s in GS.values()) + c[BIG1]*BIG1 + c[BIG2]*BIG2 )
            ret.append(sum(len(s) for s in GS.values()) + c[BIG1]*BIG1 + c[BIG2]*BIG2)
    return ret


def solve_p2_sure(y, x, max_steps, xs):
    MOVE_CACHE = {}
    ret = []
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
                # if (y, x) in MOVE_CACHE:
                    # new_locs.extend(MOVE_CACHE[(y,x)])
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
        # print(f"---{step}---")
        # for G, s in GS.items():
            # print(f"{G}", len(s))

        
        if step in xs:
            ans = sum(len(s) for s in GS.values())
            # print('    ', step, 'all', ans)
            ret.append(ans)
    return ret
# xs = list(range(20,4000))
# ys = solve_p2(sy, sx, max(xs), xs)

# print('skonczylem')


# import numpy as np

# x = np.array(xs)
# #y = np.array([16,50,1594,6536,167004,668697,16733044])
# y = np.array(ys)
# z = np.polyfit(x, y, 2)


# STEPS = 26501365
# N = STEPS
# ans = z[0]*N*N + z[1]*N+z[2]
# print('final', ans)

# print('jp dif', 631357596621921 - ans)


solve = solve_p1
W = len(M)
STEPS = 26501365
N = (STEPS - W//2) // W
# E = solve(sy, sx, 3*W)
# O = solve(sy, sx, 3*W+1)
O = 7697
E = 7730
print('E', E)
print('O', O)
print('N', N)
print('W', W)


sa = int((3*W-3) / 2)
A = solve(0,0,sa) + solve(0,W-1,sa) + solve(W-1,0,sa) + solve(W-1, W-1, sa)

sb = int((W-3)/2)
B = solve(0,0,sb) + solve(0,W-1,sb) + solve(W-1,0,sb) + solve(W-1, W-1, sb)

s = (W-1)//2
T = solve(0, s, W) + solve(s, W-1, W) + solve(W-1, s, W) + solve(s, W-1, W) 

ans = (N-1)*(N-1)*O + N*N*E + (N-1)*A + N*B + T 

print('ans:', ans)
"""
https://adventofcode.com/2023/day/22
"""

from copy import deepcopy
from collections import defaultdict


def get_unit_vector(vec):
    if vec > 0:
        return 1
    elif vec == 0:
        return 0
    else:
        return -1
    
def convert_bricks_to_list_of_points(bricks):
    bricks_as_points = []

    for sym, brick in bricks:
        sx, sy, sz = brick[0]
        ex, ey, ez = brick[1]

        dx = ex-sx
        dy = ey-sy
        dz = ez-sz

        ux = get_unit_vector(dx)
        uy = get_unit_vector(dy)
        uz = get_unit_vector(dz)
        
        px, py, pz = sx, sy, sz
        pts = []
        while (px, py, pz) != (ex, ey, ez):
            pts.append([px,py,pz])
            px += ux
            py += uy
            pz += uz
        pts.append([ex, ey, ez])

        bricks_as_points.append([sym, pts])
    
    return bricks_as_points


def esablish_map_size(bricks_as_points):
    x_max, y_max, z_max = 0, 0, 0

    for sym, bap in bricks_as_points:
        for pt in bap:
            x,y,z = pt
            x_max = max(x_max, x)
            y_max = max(y_max, y)
            z_max = max(z_max, z)
    # print(f"{x_max=}, {y_max=}, {z_max=}")
            
    return x_max, y_max, z_max


def create_empty_map(x_max, y_max, z_max):
    ZYX = []

    for zz in range(z_max+2):
        YX = []
        for yy in range(y_max+1):
            X = []
            for xx in range(x_max+1):
                X.append('.')
            YX.append(X)
        ZYX.append(YX)

    return ZYX


def can_point_fall_map(sym,x,y,z):
    if z==1:
        return False
    
    if space[z-1][y][x] == '.' or space[z-1][y][x]==sym:
        return True
    
    return False


def can_brick_fall_map(sym, bap):
    for pt in bap:
        if not can_point_fall_map(sym, *pt):
            return False
        
    return True


def gravity_on(bricks_as_points):
    global space
    changed_smth = True
    while changed_smth:
        changed_smth = False
        for sym, bap in bricks_as_points:
            bap_cp = deepcopy(bap)
            if can_brick_fall_map(sym, bap):
                changed_smth = True
                for pt in bap:
                    pt[2] -= 1
            
            #clear
            for pt in bap_cp:
                x,y,z = pt
                space[z][y][x] = '.'
            # redraw
            for pt in bap:
                x,y,z = pt
                space[z][y][x] = sym


def fill_map(bricks_as_points):
    for sym, bap in bricks_as_points:
        for pt in bap:
            x,y,z = pt
            space[z][y][x] = sym

bricks = []
sym = ord('A') - 1

with open('in.txt', 'r') as f: 
    for line in f.readlines():
        start_end = line.split('~')
        start, end = start_end
        start = [int(n) for n in start.split(',')]
        end = [int(n) for n in end.split(',')]

        sym += 1
        bricks.append((chr(sym), [start, end]))

bricks_as_points = convert_bricks_to_list_of_points(bricks)
space = create_empty_map(*esablish_map_size(bricks_as_points))
fill_map(bricks_as_points)
gravity_on(bricks_as_points)

def map_bricks_to_its_supporting_bricks(bricks_as_points):
    supports = defaultdict(set)

    for sym, brick in bricks_as_points:
        supports[sym]
        for pt in brick:
            x,y,z = pt
            if space[z+1][y][x] != '.':
                if sym != space[z+1][y][x]:
                    supports[space[z+1][y][x]].add(sym)

    return supports


supports = map_bricks_to_its_supporting_bricks(bricks_as_points)

all_bricks = set(supports.keys())
all_bricks_ = deepcopy(all_bricks)
for br, sups in supports.items():
    if len(sups) == 1:
        cant = sups.pop()
        if cant in all_bricks:
            all_bricks.remove(cant)
        sups.add(cant)

print('p1:', len(all_bricks))


destoryed_2_fall = defaultdict(int)
for brick in all_bricks_:
    supports_copy = deepcopy(supports)
    to_destroy = set()
    to_destroy.add(brick)

    seen = 0
    seen = set()
    destoryed_2_fall[brick] = -1
    while to_destroy:
        destroyed = to_destroy.pop()
        seen.add(destroyed)
        destoryed_2_fall[brick] += 1
        for b in supports_copy:
            if destroyed in supports_copy[b]:
                supports_copy[b].remove(destroyed)
                if len(supports_copy[b]) == 0 and b not in seen:
                    to_destroy.add(b)


print('p2:', sum(destoryed_2_fall.values()))

"""
https://adventofcode.com/2023/day/14
"""

from copy import deepcopy


def pm(M):
    for r in M:
        print(''.join(r))
    print()
    print()


def move_north(B):
    changed = False
    for y in range(len(B)):
        for x in range(len(B[0])):
            if B[y][x] == 'O':
                if y-1>-1:
                    if B[y-1][x] == '.':
                        B[y-1][x] = 'O'
                        B[y][x] = '.'
                        changed = True
    return changed

def move_south(B):
    changed = False
    for y in range(len(B)-1,-1, -1):
        for x in range(len(B[0])):
            if B[y][x] == 'O':
                if y+1 < len(B):
                    if B[y+1][x] == '.':
                        B[y][x] = '.'
                        B[y+1][x] = 'O'
                        changed = True
    return changed


def move_west(B):
    changed = False
    for y in range(len(B)):
        for x in range(len(B[0])):
            if B[y][x] == 'O':
                if x-1>-1:
                    if B[y][x-1]=='.':
                        B[y][x] = '.'
                        B[y][x-1] = 'O'
                        changed = True
    return changed


def move_east(B):
    changed = False
    for y in range(len(B)):
        for x in range(len(B[0])-1, -1, -1):
            if B[y][x] == 'O':
                if x+1 < len(B[0]):
                    if B[y][x+1] == '.':
                        B[y][x] = '.'
                        B[y][x+1] = 'O'
                        changed = True
    return changed


def tilt(move_function, M):
    while move_function(M):
        pass
    return M


def count_load(M):
    cnt = 0
    idx = 0
    for r in M:
        c = r.count('O')
        cnt += c*(len(M)-idx)
        idx += 1
    return cnt


def cycle(M):
    tilt(move_north, M)
    tilt(move_west,  M)
    tilt(move_south, M)
    tilt(move_east, M)
    return M


with open('in.txt', 'r') as f: 
    M = [list(l.strip()) for l in f.readlines()]

P1 = tilt(move_north, M)
print('p1:', count_load(P1))

#### p2 ####
C = 1000000000
STORAGE = []
for i in range(1, C + 1):
    M = cycle(M)
    if M in STORAGE:
        # print(f'REPEATED!! first occurance in STORAGE' 
        #       + f' at index: {STORAGE.index(M)}, next occurance in STORAGE at index: {i}')
        break
    else: 
        STORAGE.append(deepcopy(M))

loop_length = len(STORAGE) - STORAGE.index(M)
final_idx = (C % loop_length)
while final_idx < STORAGE.index(M):
    final_idx += loop_length

print(f'p2:', count_load(STORAGE[final_idx-1]))

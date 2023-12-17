"""
https://adventofcode.com/2023/day/13
"""

def find_horizontal_mirror(p):
    ans = -1
    for idx in range(len(p)):
        mirror = False

        d = 0
        while idx-d > -1 and idx+d+1<len(p):
            if p[idx-d] != p[idx+d+1]:
                mirror = False
                break
            else:
                mirror = True
            d += 1
        if mirror:
            ans = max(ans, idx)
        else:
            continue
    return ans+1


def find_vertical_mirror(p):
    ans = -1
    for x in range(len(p[0])):
        mirror = False
        for y in range(len(p)):
            d=0
            while x-d>-1 and x+d+1<len(p[0]):
                if p[y][x-d] == p[y][x+d+1]:
                    mirror = True
                else:
                    mirror = False
                    break
                d+=1
            if not mirror: break
        if not mirror: continue
        else: ans = x
    return ans+1


def find_horizontal_mirror_smudges(p):
    ans = -1
    for idx in range(len(p)):
        smudges = 0
        d = 0
        while idx-d > -1 and idx+d+1<len(p):
            for up, do in zip(p[idx-d],p[idx+d+1]):
                if up != do:
                    smudges += 1
            d += 1
        if smudges == 1:
            ans = max(ans, idx)
    return ans+1


def find_vertical_mirror_smudges(p):
    ans = -1
    for x in range(len(p[0])):
        smudges = 0
        for y in range(len(p)):
            d=0
            while x-d>-1 and x+d+1<len(p[0]):
                if p[y][x-d] != p[y][x+d+1]:
                    smudges+=1
                d+=1
        if smudges==1:
            ans = x
    return ans+1


with open('in.txt', 'r') as f: 
    lines = [l.strip() for l in f.readlines()]
lines.append('') 
patterns = []
pattern = []
for line in lines:
    if line == '':
        patterns.append(pattern)
        pattern = []
    else:
        pattern.append(line)

p1, p2 = 0, 0
for pattern in patterns:
    h1 = find_horizontal_mirror(pattern)
    v1 = find_vertical_mirror(pattern)
    p1 += 100*h1+v1

    h2 = find_horizontal_mirror_smudges(pattern)
    v2 = find_vertical_mirror_smudges(pattern)
    p2 += 100*h2+v2

print('p1:', p1)
print('p2:', p2)

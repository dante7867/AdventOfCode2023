"""
https://adventofcode.com/2023/day/8
"""


from collections import Counter
from math import gcd


with open('in.txt', 'r') as f: lines = [l.strip() for l in f.readlines()]

ins = lines[0].strip()

N = {}
lines = lines[2:]
for l in lines:
    L = l[:4].strip()
    M = l[l.find('(')+1: l.find(',')].strip()
    R = l[l.find(',')+2: l.find(')')].strip()
    N[L] = (M,R)


def move(c, instr, N): 
    if instr == 'L':
        c = N[c][0]
    else:
        c = N[c][1]
    return c 

step = 0
c = 'AAA'

step = 0
c = 'AAA'
idx = -1
while c != 'ZZZ':
    step+=1
    idx = (idx+1) % len(ins)
    c = N[c][0] if ins[idx] == 'L' else N[c][1]

print('p1:', step)
###############
def all_end_with_z(strs):
    ans = True
    for s in strs:
        if s[-1] != 'Z':
            ans = False
            break
    return ans

As = [ele for ele in N if ele[-1] =='A']


def find_cycle(n, N):
    cnt = Counter()
    cnt[(0, n)] += 1

    h = [n]
    step = 0
    idx = -1
    while True:
        step += 1
        idx = (idx+1) % len(ins)
        n = N[n][0] if ins[idx] == 'L' else N[n][1]

        cur = (idx, n)
        cnt[cur]+=1
        h += [n]
        if cnt[cur]==2:
            first, second = h.index(n), len(h) - 1 -h[::-1].index(n)
            Zs = [i for i,p in enumerate(h) if p[-1] == 'Z']
            cyc_len = second - first
            return cyc_len


def find_lcm_for_many(numbers):
    lcm = 1
    for i in numbers:
        lcm = lcm*i//gcd(lcm, i)
    return lcm


cycles = [find_cycle(a, N) for a in As]
print('p2:', find_lcm_for_many(cycles))

"""
https://adventofcode.com/2023/day/6
"""

with open('in.txt', 'r') as f: lines = [l.strip() for l in f.readlines()]
Ts = [int(x) for x in lines[0].strip().split()[1:]]
Ds = [int(x) for x in lines[1].strip().split()[1:]]


p1 = 1
for T, D in zip(Ts,Ds):
    cnt = 0
    for t in range(T):
        d = t*(T-t)
        if (d > D): cnt += 1
    p1 *= cnt
print('p1:', p1)

T = int(''.join(str(x) for x in Ts))
D = int(''.join(str(x) for x in Ds))

d = 0
p2 = 0
for t in range(T):
    d = t*(T-t)
    if (d > D): p2+=1
print('p2:', p2)

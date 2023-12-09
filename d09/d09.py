"""
https://adventofcode.com/2023/day/9
"""

with open('in.txt', 'r') as f: lines = [l.strip() for l in f.readlines()]

H = []
for line in lines:
    h = line.split()
    H.append([int(x) for x in h])
    

p1, p2 = 0, 0
for h in H:
    L = [h]
    while not all(map(lambda x: x==0, L[-1])):
        l = [j - i for i, j in zip(L[-1][:-1], L[-1][1:])]
        L.append(l)

    idx = len(L) - 1 - 1
    L[idx+1] = [0] + L[idx+1]
    while idx > -1:
        #    x y
        #     z
        # x + z = y

        y = L[idx][-1] + L[idx+1][-1]
        L[idx].append(y)

        # p2
        x =  L[idx][0] - L[idx+1][0]
        L[idx] = [x] + L[idx]
        idx -= 1
    p1 += y
    p2 += x
print('p1:', p1)
print('p2:', p2)


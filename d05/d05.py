"""
https://adventofcode.com/2023/day/5
"""

with open("in.txt", 'r') as f:
    lines = [line.strip() for line in f.readlines()] + [""]
    SEEDS = lines[0][lines[0].find(':')+2:].strip().split()
    lines = lines[2:]

SEEDS = [int(s) for s in SEEDS]
SEED_RANGES = [(int(x), int(x)+int(y)) for x, y in zip(SEEDS[::2], SEEDS[1::2])]

category = ''
categories = {}
rules = []
for line in lines:
    if ':' in line:
        category = line
    elif line == '':
        categories[category] = rules
        rules = []
    else:
        n = line.split(' ')
        rules += [(int(n[0]), (int(n[1]), int(n[1])+int(n[2])))]


def apply_rule(S: list, rule)->list:
    M = []
    R = []
    while S:
        dst, tup = rule
        c = S.pop()
        #print('\tc:', c)
        # left
        left = (c[0], min(c[1], tup[0]))
        #print('\tleft', left)
        if left[0]<left[1]:
            R.append(left)
        # inter
        dif = tup[0] - dst
        inter = (max(c[0],tup[0]), min(c[1],tup[1]))
        if inter[0] < inter[1]:
            M.append((inter[0]-dif, inter[1]-dif))
        #print('\tinter', inter)
        # right
        right = (max(c[0], tup[1]) , c[1])
        
        #print('\tright', right)
        if right[0]<right[1]:
            R.append(right)

    return R, M

for idx in range(len(SEEDS)):
    for category, rules in categories.items():
        for rule in rules:
            dst, rule_range = rule
            st, ed = rule_range
            if st<=SEEDS[idx]<ed:
                SEEDS[idx] -= st - dst
                break

print('p1:', min(SEEDS))

END = []
for seed_range in SEED_RANGES:
    S = [seed_range]
    for category, rules in categories.items():
        AM = []
        for rule in rules:
            S, M = apply_rule(S, rule)
            AM += M
        S = AM + S
    END += S


print('p2:', min(x for x,y in END))

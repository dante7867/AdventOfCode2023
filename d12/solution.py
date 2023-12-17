"""
https://adventofcode.com/2023/day/12
"""

from copy import deepcopy

with open('ex2.txt', 'r') as f: 
    lines = [l.strip() for l in f.readlines()]

LINES = []
for l in lines:
    springs  = l.split()[0]
    raport = [int(x) for x in l.split()[1].split(',')]
    print(springs, '|||', raport)
    LINES.append((springs, raport))


def create_raport(spring):
    raport = []
    cnt = 0
    for ch in spring:
        if ch == '#':
            cnt += 1
        else:
            if cnt:
                raport.append(cnt)
                cnt = 0
    if cnt:
        raport.append(cnt)

    return raport


def brute_force(spring):
    p = [spring]
    f = []
    while p:
        c = p.pop()
        i = c.find('?')
        if i > -1:
            p.append(c[:i]+'#'+c[i+1:])
            p.append(c[:i]+'.'+c[i+1:])
        else:
            f.append(c)
    # print(f)
    return f


def count_matching_possibilities(LINES):
    cnt = 0
    for s, r in LINES:  
        possibilites = brute_force(s)
        for  p in possibilites:
            if create_raport(p) == r:
                cnt += 1
    return cnt

        
print('p1', count_matching_possibilities(LINES))


### p2 ###

LINES_P2 = []       
for s, r in LINES:
    ns = '?'.join([s]*5)
    nr = r*5
    LINES_P2.append((ns, nr))


def check_raport(raport, expected):
    if len(raport) > len(expected):
        return False
    
    for i in range(len(raport)-1):
        if raport[i] != expected[i]:
            return False
    
    if raport[-1] > expected[len(raport)-1]:
        return False
    
    return True

def fill_spring(spring, expected):
    springs = [('.'+spring, [], 1)]
    cnt = 0
    while springs:
        st, raport, i = springs.pop()
        if i == len(st) or (st[i:].find('?')==-1 and st[i:].find('#')==-1):
            if raport == expected:
                cnt += 1
                continue
        for idx in range(i, len(st)):
            if st[idx] == '.':
                pass
            elif st[idx] == '#':
                if not raport:
                    raport.append(1)
                else:
                    if st[idx-1] == '#':
                        raport[-1] += 1
                    else:
                        raport.append(1)
                if(not check_raport(raport, expected)):
                    break
                else:
                    springs.append((st, deepcopy(raport), idx+1))
                    break
            elif st[idx] == '?':
                with_dot = st[:idx] + '.' + st[idx+1:]
                springs.append((with_dot, deepcopy(raport), idx + 1))
                with_hash = st[:idx] + '#' + st[idx+1:]
                if st[idx-1] == '.':
                    raport.append(1)
                else:
                    raport[-1] += 1
                if(check_raport(raport, expected)):
                    springs.append((with_hash, deepcopy(raport), idx + 1))
                break
    return cnt


print('----------p2-------------')
p2 = 0
for pair in LINES_P2:
    s, r = pair
    print(s, r)
    
    arrangements =  fill_spring(s, r)
    print(f'Arrangements: {arrangements}')
    p2 += arrangements
print('p2:', p2)

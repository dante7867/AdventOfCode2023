"""
https://adventofcode.com/2023/day/12
"""


# leaving many solutions that were to slow for part 2 for future reference


import re
import itertools

from functools import cache
from copy import deepcopy


with open('in.txt', 'r') as f: 
    lines = [l.strip() for l in f.readlines()]

SPRINGS_CACHE = {}
RAPORT_CACHE = {}
LINES = []
for l in lines:
    springs  = l.split()[0]
    raport = [int(x) for x in l.split()[1].split(',')]
    LINES.append((springs, raport))


def create_raport(spring):
    if spring in RAPORT_CACHE:
        return RAPORT_CACHE[spring]
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

    RAPORT_CACHE[spring] = raport
    return raport


def brute_force(spring):
    global SPRINGS_CACHE
    if spring in SPRINGS_CACHE:
        return SPRINGS_CACHE[spring]

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
    SPRINGS_CACHE[spring] = f
    return f


def analyze_brute_force(string, raport):
    ans = 0
    possibilites = brute_force(string)
    for  p in possibilites:
        if create_raport(p) == raport:
            ans+=1
    # print(string, raport, '->', ans)    
    return ans


def brute_force_all_possibilites_and_count_them(LINES):
    cnt = 0
    for s, r in LINES:  
        cnt += analyze_brute_force(s,r)
    return cnt


def check_raport(raport, expected):
    if len(raport) > len(expected):
        return False
    
    for i in range(len(raport)-1):
        if raport[i] != expected[i]:
            return False
    
    if raport[-1] > expected[len(raport)-1]:
        return False
    
    return True


# cuts of many possibilites but still to slow
def generate_and_count_strings_by_report(spring, expected):
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


# abandoned project =)
def of_bucket(lst, depth=0) :
	for item in lst[0] :
		if len(lst) > 1 :
			for result in of_bucket(lst[1:], depth+1) :
				yield [item,] + result
		else :
			yield [item,]


# abandoned project =)
def anaylyze(unfolded, raport):
    cnt_of_possibilites = 0
    shortened = re.sub(r'(\.)(?=\1)', '', unfolded)
    splitted = shortened.split('.')
    buckets = []
    for sp in splitted:
        raports = [create_raport(p) for p in brute_force(sp)] 
        buckets.append(raports)

        
    for n, combination in enumerate(of_bucket(buckets)) :
        joined = list(itertools.chain.from_iterable(combination))
        if joined == raport:
            cnt_of_possibilites += 1
    return cnt_of_possibilites


@cache 
def analyze_recursively(string, raport, prev):
    ans = 0
    if len(string) == 1:
        if raport == (0,) or raport==tuple():
            return 1
        else:
            return 0
    else:
        ch = string[0]
        if ch == '?':
            # dot .
            if prev == '.':
                ans += analyze_recursively(string[1:], raport, '.')
            elif prev == '#':
                if len(raport) > 0 and raport[0] == 0:
                    ans += analyze_recursively(string[1:], raport[1:], '.')
                else:
                    pass
            # hash #
            if len(raport) > 0 and raport[0] != 0:
                ans += analyze_recursively(string[1:], (raport[0]-1,) + raport[1:], '#')
        elif ch == '.':
            if prev == '.':
                ans += analyze_recursively(string[1:], raport, '.')
            else:
                if raport[0] != 0:
                    return 0
                else:
                    ans += analyze_recursively(string[1:], raport[1:], '.')
        elif ch == '#':
            if len(raport) == 0 or raport[0] == 0:
                return 0
            ans += analyze_recursively(string[1:], (raport[0]-1,) + raport[1:], '#')
    return ans


p1, p2 = 0, 0
for string, raport in LINES:
    p1 += analyze_recursively(string+'.', tuple(raport), '.')
    p2 += analyze_recursively('?'.join([string]*5)+'.', tuple(raport * 5), '.')


# print('p1 brute force:', brute_force_all_possibilites_and_count_them(LINES))

print("p1:", p1)
print("p2:", p2)
 
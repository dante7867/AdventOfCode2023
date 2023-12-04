"""
https://adventofcode.com/2023/day/4
"""

from collections import Counter


with open('in.txt', 'r') as f: lines = [l.strip() for l in f.readlines()]

pts = 0
cards = {}
cnt = Counter()


def get_matching(win, have):
    c = 0
    for w in win:
        if w in have:
            c+=1
    return c


def get_pts(win, have):
    c = get_matching(win, have)
    if c == 0:
        return 0
    else:
        return 2**(c-1)


for line in lines:
    i = line.find(':')

    card = line[:i]
    card = (int(card.split()[1]))

    line = line[i+1:]
    win, have = line.split('|')
    win = win.strip().split(' ')
    win = [int(n) for n in win if n.isnumeric()]
    have=have.strip().split(' ')
    have = [int(n) for n in have if n.isnumeric()]
    cards[card] = (win, have)
    cnt[card] += 1
    pts += get_pts(win, have) 

print('p1', pts)


################## P2 ##################
current = Counter()
for c in cards:
    current[c] += 1
while sum(current.values()) != 0:
    for ca,v in current.items():
        win, have = cards[ca]
        m = get_matching(win, have)
        if m > 0:
            for n in range(ca+1, ca+1+m):
                current[n] += v
                cnt[n] += v
        current[ca] = 0

print('p2', sum(cnt.values()))

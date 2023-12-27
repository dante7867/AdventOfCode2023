"""
https://adventofcode.com/2023/day/7
"""
from collections import Counter
from functools import cmp_to_key

with open('in.txt', 'r') as f: lines = [l.strip() for l in f.readlines()]
lines = [line.strip().split() for line in lines]

CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
TYPE_2_STRENGTH = {
        (5,):7,
        (4,1):6,
        (3,2):5,
        (3,1,1):4,
        (2,2,1):3,
        (2,1,1,1):2,
        (1,1,1,1,1):1
}


def get_type(hand):
    cnt=Counter()
    for h in hand:
        cnt[h] += 1

    l = list(cnt.values())
    l.sort(reverse=True)
    return tuple(l)


def get_type_with_jokers(hand):
    cnt=Counter()
    jokers = 0
    for h in hand:
        if h!='J':
            cnt[h] += 1
        else:
            jokers += 1

    l = list(cnt.values())
    l.sort(reverse=True)
    if l:
        l[0] += jokers # get best benefit from jokers
    else:
        return (5,)
    return tuple(l)


def compare(tup1, tup2):
    if tup1[0] != tup2[0]:
        return tup1[0]-tup2[0]
    else:
        for s1, s2 in zip(tup1[1], tup2[1]):
            i1 = CARDS.index(s1)
            i2 = CARDS.index(s2)
            if i1 != i2:
                return i2-i1
        return 0


def establish_importance(hand, bid):
    t2s = []
    typ = get_type(hand)
    importance =  TYPE_2_STRENGTH[typ]
    return (importance, hand, int(bid))


def establish_importance_with_jokers(hand, bid):
    t2s = []
    typ = get_type_with_jokers(hand)
    importance =  TYPE_2_STRENGTH[typ]
    return (importance, hand, int(bid))


p1 = 0
hands_with_importance= [establish_importance(hand, bid) for hand, bid in lines]
ordered_hands_with_importance = sorted(hands_with_importance, key=cmp_to_key(compare))
for i, tup in enumerate(ordered_hands_with_importance,1):
    bid = tup[2]
    p1 += i*bid
print('p1', p1)


p2 = 0
# joker is least powerful
CARDS.remove('J')
CARDS.append('J')

hands_with_importance_jokers = [establish_importance_with_jokers(hand, bid) for hand, bid in lines]
ordered_hands_with_importance_jokers = sorted(hands_with_importance_jokers, key=cmp_to_key(compare))

for i, tup in enumerate(ordered_hands_with_importance_jokers,1):
    bid = tup[2]
    p2 += i*bid

print('p2', p2)

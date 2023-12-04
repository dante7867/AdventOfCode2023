"""
https://adventofcode.com/2023/day/1
"""


def decrypt_code(code: str) -> int:
    left, right = 0, 0
    for ch in code:
        if ch.isdigit():
            left = ch
            break
    for ch in code[::-1]:
        if ch.isdigit():
            right = ch
            break
    return 10 * int(left) + int(right)


def p1(code):
    s = 0
    for code in code:
        s += decrypt_code(code)
    print(f"p1: {s}")


########## P2 ###########


def get_rightmost_number(line: str, SYMBOLS: dict) -> int:
    idx = len(line)-1
    while idx > -1:
        if line[idx].isdigit():
            return int(line[idx])
        for n in SYMBOLS:
            if line[idx:].startswith(n):
                return SYMBOLS[n]
        idx -= 1        


def get_leftmost_number(line: str, SYMBOLS:dict) -> int:
    idx = 0
    while idx < len(line):
        if line[idx].isdigit():
            return int(line[idx])
        for n in SYMBOLS:
            if line[idx:].startswith(n):
                return SYMBOLS[n]
        idx += 1
        

def p2(codes):
    SYMBOLS = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9 
    }

    s = 0
    for code in codes:
        s += 10*get_leftmost_number(code, SYMBOLS) + get_rightmost_number(code, SYMBOLS)
    print(f"p2: {s}")


with open('in.txt', 'r') as f: 
    codes = [l.rstrip('\n') for l in f.readlines()]

p1(codes)
p2(codes)

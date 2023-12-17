"""
https://adventofcode.com/2023/day/15
"""

with open('in.txt', 'r') as f: 
    init_sequence = f.readline()
    steps = init_sequence.split(',')
    steps = [s.strip() for s in steps]


def decode_string(step):
    cv = 0
    for ch in step:
        cv += ord(ch)
        cv *= 17
        cv = cv % 256
    return cv

p1 = 0
for step in steps:
    p1 += decode_string(step)

print('p1:', p1)

BOXES = {}
for step in steps:
    op = '=' if '=' in step else '-'
    label = step[:step.find(op)]
    num = step[step.find(op)+1:]
    # print(f"{step=} -> {label}, {op}, {num}")
    bn = decode_string(label)

    if bn not in BOXES:
        BOXES[bn] = []

    box = BOXES[bn]
    if op == '=':
        changed = False
        for idx in range(len(box)):
            if box[idx][0] == label:
                box[idx][1] = num
                changed = True
        if not changed:
            box.append([label, num])
    elif op == '-':
        for_del = -1
        for idx in range(len(box)):
            l, f = box[idx]
            if l == label:
                for_del = idx
        if for_del > -1:
            del box[for_del]


p2 = 0
for n, box in BOXES.items():
    slot = 1
    for l, f in box:
        p2 += (n+1) * slot * int(f)
        slot += 1
print('p2:', p2)

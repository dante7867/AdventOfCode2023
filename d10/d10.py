"""
https://adventofcode.com/2023/day/10
"""


def get_start(m):
    for y, row in enumerate(m):
        if 'S' in row:
            return y, row.find('S')


def around(M, y, x):
    ans = []
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            ans.append((y+dy, x+dx))
    ans.remove((y, x))
    return ans


def where_can_i_move(M, cy, cx):
    pos_vecs = SYM_2_MOVE[M[cy][cx]]
    pts = []
    for v in pos_vecs:
        dy, dx = v
        ny = cy + dy
        nx = cx + dx
        if M[ny][nx] in SYM_2_MOVE:
            # are the pipes connected (aka can I move back)
            if (-dy,-dx) in SYM_2_MOVE[M[ny][nx]]:
                #print(f'You can go to M[{ny}][{nx}]')
                pts.append((ny,nx))
    return pts


def move(M, y, x, prev_y, prev_x, step):
    dests = where_can_i_move(M, y, x)
    dests = [d for d in dests if d!=(prev_y, prev_x)]
    return dests[0][0], dests[0][1], y, x, step + 1


SYM_2_MOVE = {
    'S': [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)],
    '|': [(-1,0),(1,0)],
    '-': [(0,-1), (0, 1)],
    'L': [(-1,0), (0, 1)],
    'J': [(-1,0), (0, -1)],
    '7': [(0,-1), (1, 0)],
    'F': [(0,1),(1,0)]
}

with open('in.txt', 'r') as f: 
    M = [l.strip() for l in f.readlines()]

sy, sx = get_start(M)
y = sy
x = sx
prev_y = -1
prev_x = -1
step = 0
loop_parts = set()
loop_parts.add((y, x))
while True:
    y, x, prev_y, prev_x, step = move(M, y, x, prev_y, prev_x, step)
    loop_parts.add((y, x))
    if M[y][x] == 'S':
        print("p1:", step//2)
        break

M2 = []
for y in range(len(M)):
    L = ''
    for x in range(len(M[0])):
        L += M[y][x] if (y,x) in loop_parts else '.'
    M2.append(L)


for i in range(len(M2)):
    M2[i] = list(M2[i])


ZOOMS = {
    'S': [['S', 'S', 'S'],
          ['S', 'S', 'S'],
          ['S', 'S', 'S']],

    '|': [['.', '|', '.'],
          ['.', '|', '.'],
          ['.', '|', '.']],

    '-': [['.', '.', '.'],
          ['-', '-', '-'],
          ['.', '.', '.']],
          
    'L': [['.', '|', '.'],
          ['.', '|', '_'],
          ['.', '.', '.']],
          
    'J': [['.', '|', '.'],
          ['_', '|', '.'],
          ['.', '.', '.']],
          
    '7': [['.', '.', '.'],
          ['-', '|', '.'],
          ['.', '|', '.']],
          
    'F': [['.', '.', '.'],
          ['.', '|', '-'],
          ['.', '|', '.']],

    '.': [['.', '.', '.'],
          ['.', '?', '.'],
          ['.', '.', '.']]        
}

ZM = []
for row in M2:
    ls = [[], [], []]
    for symbol in row:
        for i in range(len(ls)):
            ls[i] += ZOOMS[symbol][i]
    for l in ls:
        ZM.append(l)

# starting from top left corner flood map with 'O' symbol
sy, sx = 0, 0
new = [(sy, sx)]
M2[sy][sx] = 'O'
while new:
    n = new.pop()
    y, x = n
    for dy in [-1,0,1]:
        for dx in [-1,0,1]:
            if dx==dy==0:
                continue
            else:
                if 0 <= y+dy < len(ZM) and 0<= x+dx < len(ZM[0]):
                    if ZM[y+dy][x+dx] in '.?':
                        ZM[y+dy][x+dx] = 'O'
                        new.append((y+dy, x+dx))

# count '?' that can be found after zooming 1 per '.' block that where not flooded
cnt = 0
for row in ZM:
    for ch in row:
        if ch == '?':
            cnt+=1
print('p2', cnt)

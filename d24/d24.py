"""
https://adventofcode.com/2023/day/24
"""

import z3


input_file = 'in.txt'
with open(input_file, 'r') as f: 
    lines = [l.strip() for l in f.readlines()]

if input_file == 'ex.txt':
    LOW = 7
    HIGH = 27
elif input_file == 'in.txt':
    LOW = 200000000000000
    HIGH = 400000000000000

HAILSTONES = []
for line in lines:
    line = line.replace(' @', ',')
    pos_velo = [int(x) for x in line.split(',')]
    HAILSTONES.append(pos_velo)

def find_intersection(a1, b1, c1, a2, b2, c2):
    # print(a1, b1, c1, a2, b2, c2)
    if a1*b2==a2*b1:
        iy = None
        ix = None
    else:
        ix = (b1*c2-b2*c1)/(a1*b2-a2*b1)
        iy = (c1*a2-c2*a1)/(a1*b2-a2*b1)
    # print('iy:', iy, ' ix:', ix)
    return iy, ix


def if_intersect_in_area(a1, b1, c1, a2, b2, c2, lower, higher):
    iy, ix = find_intersection(a1, b1, c1, a2, b2, c2)
    if iy!=None and ix!=None: #not parallel
        return lower<=iy<=higher and lower<=ix<=higher
    return False #paralel


def get_linear_equasion_from_two_points(y1, x1, y2, x2):
    a = y2-y1
    b = x1-x2
    c = y1*(x2-x1)-(y2-y1)*x1

    return a, b, c

line_equasions = []
for pos_velo in HAILSTONES:
    px, py, pz, vx, vy, vz = pos_velo
    a,b,c = get_linear_equasion_from_two_points(py, px, py+vy, px+vx)
    line_equasions.append((a,b,c))

# print(line_equasions)


cnt = 0

for i, hailstoneA in enumerate(HAILSTONES):
    for j, hailstoneB in enumerate(HAILSTONES):
        if i!=j:
            pxA, pyA, pzA, vxA, vyA, vzA = hailstoneA
            leqA = get_linear_equasion_from_two_points(pyA,pxA, pyA+vyA,pxA+vxA)
            pxB, pyB, pzB, vxB, vyB, vzB = hailstoneB
            leqB = get_linear_equasion_from_two_points(pyB,pxB, pyB+vyB,pxB+vxB)
            # print('hailstone A:', hailstoneA, ' ,leq:', leqA)
            # print('hailstone B:', hailstoneB, ' ,leq:', leqB)
            a1, b1, c1 = leqA
            a2, b2, c2 = leqB
            iy, ix = find_intersection(a1, b1, c1, a2, b2, c2)
            is_in_area = if_intersect_in_area(a1, b1, c1, a2, b2, c2, LOW, HIGH)
            # s = so+v*t => t = (s-so)/v, known: s=y1, so=py, v=vy, unknown = t

            tyA=-1
            if iy: # not paralel
                tyA = (iy-pyA)/vyA


            txA=-1
            if ix: # not paralel
                txA = (ix-pxA)/vxA

            tyB=-1
            if iy: # not paralel
                tyB = (iy-pyB)/vyB

            txB=-1
            if ix: # not paralel
                txB = (ix-pxB)/vxB

            in_future = (tyA>=0) and (txA>=0) and (tyB>=0) and (txB>=0)

            if is_in_area and in_future:
                cnt += 1

print('p1:', cnt//2)


# something new i learned thanks to reddit
def z3_solve_part2(hailstones):
    x = z3.Int('x')
    y = z3.Int('y')
    z = z3.Int('z')
    vx = z3.Int('vx')
    vy = z3.Int('vy')
    vz = z3.Int('vz')

    solver = z3.Solver()

    for i, hailstone in enumerate(hailstones):
        px, py, pz, pvx, pvy, pvz = hailstone
        t = z3.Int("t"+str(i))
        solver.add(x + vx*t == px+pvx*t)
        solver.add(y + vy*t == py+pvy*t)
        solver.add(z + vz*t == pz+pvz*t)
    
    solver.check()
    
    return solver.model().eval(x+y+z)

print('p2:', z3_solve_part2(HAILSTONES))

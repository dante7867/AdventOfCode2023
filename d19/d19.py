"""
https://adventofcode.com/2023/day/19
"""

with open('in.txt', 'r') as f: 
    lines = [l.strip() for l in f.readlines()]

WORKFLOWS, PARTS = {}, []
empty_met =  False
for l in lines:
    if l == "":
        empty_met = True
        continue
    if not empty_met:
        wf_name = l[:l.find('{')]
        operations = l[l.find('{')+1:-1]
        WORKFLOWS[wf_name] = operations.split(',')
    else:
        l = l[1:-1]
        ratings = l.split(',')
        p = {}
        for rat in ratings:
            p[rat[0]] = int(rat[2:])
        PARTS.append(p)

# print(WORKFLOWS)
# print(PARTS)


def do_workflow(x,m,a,s, workflow):
    # print(x,m,a,s, workflow)
    for operation in workflow:
        splitted = operation.split(':')
        # print(splitted)
        if len(splitted) == 1:
            return splitted[0]
        elif len(splitted) == 2:
            condition, result = splitted[0], splitted[1]
            if eval(condition):
                return result


def is_part_accepted(x,m,a,s):
    current_workflow = 'in'
    while current_workflow not in 'RA':
        current_workflow = do_workflow(x,m,a,s, WORKFLOWS[current_workflow])
    if current_workflow == 'A':
        return True
    return False

p1 = 0
for part in PARTS:
    x = part['x']
    m = part['m']
    a = part['a']
    s = part['s']
    
    if is_part_accepted(x,m,a,s):
        p1+= x + m + a + s

print('p1:', p1)


######################################################
####################### PART 2 #######################
######################################################


# returns match rest match, rest
def divide_tuple(divisor, sign, divider):
    st, ed = divisor[0], divisor[1]
    if sign == '>':
        return (divider+1, ed), (st, divider)
    elif sign == '<':
        return (st, divider-1), (divider, ed)

# operation ex: hmm op_arg = ('in', (1,5), (1,5), (1,5),(3,7))
# returns:
#   [
#       [('hmm'),(1-5), (1,3), (1,5), (3,7)]
#   ]
#
#
# operation ex: m>3:lol, op_arg = ('in', (1,5), (1,5), (1,5),(3,7))
# returns:
#   [
#                        !!!
#       [('lol', (1-5), (4,5), (1,5), (3,7)] # goes to 'lol' op
#       [('???'),(1-5), (1,3), (1,5), (3,7)] # goes to next instruction
#   ]
def do_operation(operation, x,m,a,s):
    if ':' not in operation: # there will be NO condition
        return [[(operation),x,m,a,s], 'NOTHING LEFT']
    else:
        splitted = operation.split(':')
        condition, action = splitted
        sign = '>' if '>' in condition else '<'
        assert sign in '><'
        divider = int(condition[condition.find(sign)+1:])
        if condition[0] == 'x':
            match, rest = divide_tuple(x, sign, divider)
            return [
                [action, match, m, a, s],
                ['???', rest, m, a, s]
            ]
        elif condition[0] == 'm':
            match, rest = divide_tuple(m, sign, divider)
            return [
                [action, x, match, a, s],
                ['???', x, rest, a, s]
            ]
        elif condition[0] == 'a':
            match, rest = divide_tuple(a, sign, divider)
            return [
                [action, x, m, match, s],
                ['???', x, m, rest, s]
            ]
        elif condition[0] == 's':
            match, rest = divide_tuple(s, sign, divider)
            return [
                [action, x, m, a, match],
                ['???', x, m, a, rest]
            ]
        
assert [['hmm', (1,5), (1,5), (1,5),(3,7)], 'NOTHING LEFT']==do_operation('hmm', (1,5), (1,5), (1,5),(3,7))

# x
assert [['lol', (4,5), (1,5), (1,5),(3,7)], ['???', (1,3), (1,5), (1,5),(3,7)]]==do_operation('x>3:lol', (1,5), (1,5), (1,5),(3,7))
assert [['lol', (1,2), (1,5), (1,5),(3,7)], ['???', (3,5), (1,5), (1,5),(3,7)]]==do_operation('x<3:lol', (1,5), (1,5), (1,5),(3,7))
# m
assert [['lol', (1,5), (4,5), (1,5),(3,7)], ['???', (1,5), (1,3), (1,5),(3,7)]]==do_operation('m>3:lol', (1,5), (1,5), (1,5),(3,7))
assert [['lol', (1,5), (1,2), (1,5),(3,7)], ['???', (1,5), (3,5), (1,5),(3,7)]]==do_operation('m<3:lol', (1,5), (1,5), (1,5),(3,7))
# a
assert [['lol', (1,5), (1,5), (4,5),(3,7)], ['???', (1,5), (1,5), (1,3),(3,7)]]==do_operation('a>3:lol', (1,5), (1,5), (1,5),(3,7))
assert [['lol', (1,5), (1,5), (1,2),(3,7)], ['???', (1,5), (1,5), (3,5),(3,7)]]==do_operation('a<3:lol', (1,5), (1,5), (1,5),(3,7))
# s
assert [['lol', (1,5), (1,5), (1,5), (4,7)], ['???', (1,5), (1,5), (1,5),(3,3)]]==do_operation('s>3:lol', (1,5), (1,5), (1,5),(3,7))
assert [['lol', (1,5), (1,5), (1,5), (3,2)], ['???', (1,5), (1,5), (1,5),(3,7)]]==do_operation('s<3:lol', (1,5), (1,5), (1,5),(3,7))



MAX = 4000
wf_args = [('in', (1, MAX), (1, MAX), (1, MAX), (1, MAX))]

p2 = []
a_cnt = 0
r_cnt = 0

def test_count_possibilites(wf_args):
    total = 0
    for wf, x, m, a,s in wf_args:
        possis = (x[1]-x[0]+1)*(m[1]-m[0]+1)*(a[1]-a[0]+1)*(s[1]-s[0]+1)
        total += possis
    return total


while wf_args:
    present_possibilites = a_cnt+r_cnt+test_count_possibilites(wf_args)
    assert 4000**4==present_possibilites
    wf, x, m, a, s = wf_args.pop()
    operations = WORKFLOWS[wf]

    for op in operations:
        match, rest = do_operation(op, x, m, a, s)
        if match[0] == 'A':
            _, xx, mm, aa, ss = match
            matches = (xx[1]-xx[0]+1)*(mm[1]-mm[0]+1)*(aa[1]-aa[0]+1)*(ss[1]-ss[0]+1)
            p2 += [matches]
            a_cnt += matches
        elif match[0] == 'R':
            _, xx, mm, aa, ss = match
            matches = (xx[1]-xx[0]+1)*(mm[1]-mm[0]+1)*(aa[1]-aa[0]+1)*(ss[1]-ss[0]+1)
            r_cnt += matches
            pass
        else:
            wf_args.append(match)
        if rest != 'NOTHING LEFT':
            _, x, m, a, s = rest

print('p2:', a_cnt)

"""
https://adventofcode.com/2023/day/19
"""


with open('in.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]


MODULES = {}
for line in lines:
    s = line.split('->')
    sender, receivers = s
    sender = sender.strip()
    receivers = receivers.strip(' %\n&')
    receivers = receivers.split(',')
    receivers = [r.strip() for r in receivers]
    # print(sender, receivers)
                        
                        
                                 #[name,               type     , {ins}, [outs]   , state, state_history]
    MODULES[sender.strip('%&')] = [sender.strip('%&'), sender[0], {}   , receivers, False, [False]]

NAME = 0
TYPE = 1
INS = 2
OUTS = 3
STATE = 4
STATE_HISTORY = 5

LOW = 0
HIGH = 1

not_present = []
for name, module in MODULES.items():
    for o in module[OUTS]:
        if o in MODULES:
            MODULES[o][INS][name] = LOW
        else:
            not_present.append((o, name))

for o, src in not_present:
    if o not in MODULES:
        MODULES[o] = [o, o[0], {}, [], False, [False]]
        MODULES[o][INS][src] = False
    else:
        MODULES[o][INS][src] = False

        
def print_signal(src, sig, dst):
    sig_str = 'high' if sig else 'low'
    print(f"signal: {src} -{sig_str}-> {dst}")
  

low_cnt = 0
high_cnt = 0
press = 0

#         rx
#         | (low)
#        &zp
#         |
#    ------------
#    |(high)   |(high)     |(high)   |(high) 
#   &sb        &nd         &ds       &hf

# if 'sb','nd','ds' and 'hf' synchronize in step to send (high) zp will send (low) and turn on rx machine
# We need to find a cycle length for them and find when do they meet
CYCLES = {"sb": 0, "nd": 0, "ds": 0, "hf": 0}


while True:
    press += 1
    # print(press)
    if press == 1000 + 1:
        print('p1:', high_cnt * low_cnt)
        
    SIGNALS = [('button', LOW, 'broadcaster')]

    signals_in_step = 0
    while SIGNALS:
        current_signal = SIGNALS.pop(0)
        signals_in_step += 1
        
        src, sig, dest = current_signal
        
        # increase counter of proper signals
        if sig == HIGH:
            high_cnt += 1
        else:
            low_cnt += 1
            
        # handle signal
        if MODULES[dest][TYPE] == '%': #flip-flop
            if sig == HIGH:
                pass
            elif sig == LOW:
                MODULES[dest][STATE] = not MODULES[dest][STATE]
                
                new_sig = HIGH if MODULES[dest][STATE] else LOW
                for out in MODULES[dest][OUTS]:
                    SIGNALS.append((dest, new_sig, out))
                    # print_signal(dest, new_sig, out)
        elif MODULES[dest][TYPE] == '&':
            MODULES[dest][INS][src] = sig
            
            new_sig = LOW if all(MODULES[dest][INS].values()) else HIGH
            for out in MODULES[dest][OUTS]:
                # sig_str = 'HIGH' if new_sig else '_LOW'
                # print('&', dest, f'sends: {sig_str} to ', out ,' in press:', press, 'with singals_in_step:', signals_in_step)
                if dest in CYCLES and new_sig == HIGH:
                    CYCLES[dest] = press
                if all(CYCLES.values()):
                    ans_p2 = 1
                    for k,v in CYCLES.items():
                        ans_p2 *= v
                    print('p2:', ans_p2)
                    exit()
                SIGNALS.append((dest, new_sig, out))
                # print_signal(dest, new_sig, out)
            
        elif MODULES[dest][NAME] == 'broadcaster':
            for out in MODULES[dest][OUTS]:
                SIGNALS.append((dest, sig, out))
                # print_signal(dest, sig, out)
        elif MODULES[dest][NAME] == 'rx':
            if sig == LOW:
                print('p2:', press)
                exit()
                

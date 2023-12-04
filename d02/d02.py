"""
https://adventofcode.com/2023/day/2
"""

import re


def count_balls(pattern, txt):
    balls = re.findall(pattern, txt)
    return int(balls[0]) if len(balls) != 0 else 0


LIMITS = { "red": 12, "green": 13, "blue": 14 };
with open('in.txt', 'r') as f:
    games = f.readlines()

p1, p2 = 0, 0
for i, game in enumerate(games, 1):
    throws = game.split(';')
    is_possible = True
    max_red, max_blue, max_green = 0, 0, 0
    for throw in throws:
        blue = count_balls("(\d+)\sblue", throw) 
        green = count_balls("(\d+)\sgreen", throw)
        red = count_balls("(\d+)\sred", throw)

        if not (blue <= LIMITS["blue"] and green <= LIMITS["green"] and red <= LIMITS["red"]):
            is_possible = False

        max_blue = max(blue, max_blue)
        max_green= max(green, max_green)
        max_red = max(red, max_red)

    if is_possible:
        p1 += i

    p2 += max_red * max_green * max_blue

print('p1', p1)
print('p2', p2)

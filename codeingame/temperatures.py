# Patryk Kośmider s16863
# https://www.codingame.com/ide/puzzle/temperatures

import math

n = int(input())

if n != 0:
    closest = 5526

    for i in input().split():
        t = int(i)

        if abs(t) < abs(closest):
            closest = t
        elif abs(t) == abs(closest):
            closest = t if closest < 0 else abs(t)

    print(closest)
else:
    print(0)

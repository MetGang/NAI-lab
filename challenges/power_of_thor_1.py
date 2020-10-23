# https://www.codingame.com/ide/puzzle/power-of-thor-episode-1

import math

dstX, dstY, x, y = [ int(i) for i in input().split() ]

def sign(x):
    return (x > 0) - (x < 0)

hName = [ 'W', '', 'E' ]
vName = [ 'N', '', 'S' ]

while True:
    remaining_turns = int(input())

    signX = sign(dstX - x)
    signY = sign(dstY - y)

    print(vName[signY + 1] + hName[signX + 1])

    x += signX
    y += signY

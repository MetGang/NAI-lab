# https://www.codingame.com/ide/puzzle/power-of-thor-episode-1

import math

dst_x, dst_y, x, y = [ int(i) for i in input().split() ]

def sign(x):
    return (x > 0) - (x < 0)

h_name = [ 'W', '', 'E' ]
v_name = [ 'N', '', 'S' ]

while True:
    remaining_turns = int(input())

    sign_x = sign(dst_x - x)
    sign_y = sign(dst_y - y)

    print(v_name[sign_y + 1] + h_name[sign_x + 1])

    x += sign_x
    y += sign_y

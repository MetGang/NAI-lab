# https://www.codingame.com/ide/puzzle/the-descent

import math

while True:
    order = True
    heights = [ 0 ] * 8

    for i in range(8):
        heights[i] = int(input())

    max_value = max(heights)

    if order:
        print(heights.index(max_value))
    else:
        print(heights.index(max_value, 7, 0))

    order = not order

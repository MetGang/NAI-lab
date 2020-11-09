# Patryk Kośmider s16863
# https://www.codingame.com/ide/puzzle/the-descent

import math

while True:
    height = 0
    index = 0

    for i in range(8):
        h = int(input())
        if h > height:
            height = h
            index = i
    
    print(index)

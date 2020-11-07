# Patryk Kośmider s16863
# https://www.codingame.com/ide/puzzle/ascii-art

import math

w = int(input())
h = int(input())
text = input()

def ascii_to_index(ch):
    if ord(ch) >= ord('A') and ord(ch) <= ord('Z'):
        return ord(ch) - ord('A')
    if ord(ch) >= ord('a') and ord(ch) <= ord('z'):
        return ord(ch) - ord('a')
    return ord('Z') - ord('A') + 1

for i in range(h):
    row = input()
    
    for ch in text:
        index = ascii_to_index(ch) * w
        print(row[index : index + w], end = '')

    print()

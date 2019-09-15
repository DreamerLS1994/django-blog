#! /usr/bin/python3

#coding utf-8

import random, string

def getrandom(x):
    return random_codes(poolOfChars, x)
    
poolOfChars  = string.ascii_letters + string.digits
random_codes = lambda x, y: ''.join([random.choice(x) for i in range(y)])

with open('/root/ssrcode.txt', 'w') as fw:
    fw.write(getrandom(5))


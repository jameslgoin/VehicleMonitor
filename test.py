#!/usr/bin/python3
import random, time


x = random.randint(0,180)
while True:
    print('speed:%i' % x, flush=True)
    x = random.randint(0, 180)
    time.sleep(1)

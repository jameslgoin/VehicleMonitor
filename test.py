#!/usr/bin/python3
import random, time


get_speed = lambda : random.randint(0,180)
get_light = lambda : random.choice(['L', 'N', 'R'])
get_gear = lambda : random.choice(['P', 'R', 'N', 'D'])
get_acc = lambda : random.uniform(0, 1)
get_break = lambda : random.uniform(0, 1)


while True:
    print('speed:%i' % get_speed(), flush=True)
    print('light:%s' % get_light(), flush=True)
    print('gear:%s' % get_gear(), flush=True)
    print('accelerator:%f' % get_acc(), flush=True)
    print('break:%f' % get_break(), flush=True)
    time.sleep(1)

import time, random


x = random.randint(0,180)
while True:
    print('speed:%i' % x)
    x = random.randint(0, 180)
    time.sleep(1)
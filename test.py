import time, random


x = random.randint(0,300)
while True:
    print('speed:%i' % x)
    x = random.randint(0, 300)
    time.sleep(1)
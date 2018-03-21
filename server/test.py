#!/usr/bin/python3
import random, time
from threading import Thread


get_speed = lambda : random.randint(0,180)
get_0_1 = lambda : random.uniform(0, 1)
get_string = lambda : 'Random String ' + random.randint(0,1000)
get_pos = lambda : random.randint(100000,1000000)
get_whl = lambda : random.randint(-180,180)


class MyThread(Thread):
    def __init__(self, template, gen, interval):
        Thread.__init__(self)
        self.template = template
        self.gen = gen
        self.interval = interval
        self.daemon = True

    def run(self):
        while True:
            print(self.template % self.gen(), flush=True)
            time.sleep(self.interval)

    def start(self):
        Thread.start(self)
        return self

VehSpdAvgDrvn = MyThread('VehSpdAvgDrvn:%i', get_speed, 0.1).start()
AccPos = MyThread('AccPos:%f', get_0_1, 0.2).start()
BrkPdlPos = MyThread('BrkPdlPos:%f', get_0_1, 0.3).start()
EngOilRmnLf = MyThread('EngOilRmnLf:%f', get_0_1, 0.4).start()
PsngSysLat = MyThread('PsngSysLat:%i', get_pos, 0.5).start()
PsngSysLong = MyThread('PsngSysLong:%i', get_pos, 0.5).start()
StrWhAng = MyThread('StrWhAng:%i', get_whl, 0.5).start()
TrnSwAct = MyThread('TrnSwAct:%i', lambda : random.choice([0,1,2,3]), 0.6).start()
TrnsShftLvrPos = MyThread('TrnsShftLvrPos:%i', lambda : random.choice([1, 2, 3, 4]), 0.6).start()

while True:

    time.sleep(5.5)

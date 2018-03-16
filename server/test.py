#!/usr/bin/python3
import random, time


get_speed = lambda : random.randint(0,180)
get_0_1 = lambda : random.uniform(0, 1)
get_string = lambda : 'Random String ' + random.randint(0,1000)
get_pos = lambda : random.randint(100000,1000000)
get_whl = lambda : random.randint(-180,180)



while True:
    print('VehSpdAvgDrvn:%i' % get_speed())
    print('AccPos:%f' % get_0_1())
    print('BrkPdlPos:%f' % get_0_1())
    print('EngOilRmnLf:%f' % get_0_1())

    print('PsngSysLat:%i' % get_pos())
    print('PsngSysLong:%i' % get_pos())

    print('StrWhAng:%i' % get_whl())
    print('TrnSwAct:%i' % random.choice([1,2]))
    print('TrnsShftLvrPos:%i' % random.choice([1, 2, 3, 4]), flush=True)

    time.sleep(1)

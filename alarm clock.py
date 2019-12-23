#!/usr/bin/env python
# Program that waits untill a given time to play an alarm
#
# Copywrite Cat Inc, All rights reserved.
# Programmed by Samuel Davenport, member of Cat Inc.
import time

class doMath:  
    def seperate(text):
        ftimes = 0
        scan = str(' ' + str(text))
        for i in scan:
            if str(i) == ' ':
                ftimes = ftimes + 1
                what = str('tmp' + str('i' * int(ftimes)))
                exec(str(what + " = ''"))
            else:
                what = str('tmp' + str('i' * int(ftimes)))
                tostore = str(eval(what) + str(i))
                exec(str(what + " = '" + tostore + "'"))
        tmp = []
        for i in range(ftimes):
            what = str('tmp' + str('i' * int(i + 1)))
            tmp.append(str(eval(what)))
        return list(tmp)
    
    def septime(timein):
        global hour
        global minit
        varz = ('hour', 'minit')
        sel = 0
        for i in range(len(varz)):
            exec(str(varz[sel]) + ' = []')
            sel += 1
        sel = 0
        datime = str(timein)
        datime = list(datime)
        for i in range(len(datime) - 3):
            if datime[i] == ':':
                sel += 1
            else:
                exec(str(varz[sel])+'.append(datime[i])')
        sel = 0
        for i in range(len(varz)):
            exec(str(varz[sel])+ " = ''.join(" + str(varz[sel]) + ')')
            sel += 1
        toret = []
        sel = 1
        for i in range(len(varz)):
            print("toret.append(str(" + str(eval(varz[sel - 1])) + '))')
            exec("toret.append(str(" + str(eval(varz[sel - 1])) + '))')
            if sel != 2:
                sel -= 1
        return toret
    pass

def waituntil(timein):
    ctime = doMath.seperate(str(time.asctime()))[4]
    while ctime != timein:
        ctime = doMath.seperate(str(time.asctime()))[4]
        time.sleep(1)

stime = doMath.seperate(str(time.asctime()))[4]
waituntil('06:30:00')

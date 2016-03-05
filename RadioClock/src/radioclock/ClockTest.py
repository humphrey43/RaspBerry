'''
Created on 07.02.2016

@author: hardy
'''
from radioclock import classes
from radioclock import player
from radioclock import clockwork

if __name__ == '__main__':
#    classFactory = classes.ClassFactory()
#    clockwork.init()
#    player.init()
    
#    cf.register("Alarm", clockwork.Alarm)
#    cf.register("AlarmType", clockwork.AlarmType)
#    cf.register("Source", player.Source)
    a = clockwork.Alarm()
    s = classes.toJSON(a)
    print s
    setattr(a, "minute", 7)
    s = classes.toJSON(a)
    print s
    b = classes.createInstance(s)
    s = classes.toJSON(b)
    print s
   

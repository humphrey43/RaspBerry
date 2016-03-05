'''
Created on 09.02.2016

@author: hardy
'''
from time import *
from datetime import datetime
import logger

logger.logfile = 'C:/Temp/RadioClock.log'
t=localtime()
print(t)
wt = t.tm_wday
print(wt)
i = "MO#DI#MI#DO#FR#SA#SO#".find("DI")
print i //3 

logger.log("start")

class EventSource:
           
    def __init__(self, func):
        self.func = func
        print "__init__\n"
        pass
        
    def __call__(self, *args, **kwargs):
        print "__call1__\n"
        self.func(*args, **kwargs)
        print "__call2__\n"
        pass

@EventSource
def func(i, *args, **kwargs):
    print "in func: " + str(i)  + "\n"
    print args
    print kwargs

@EventSource
def func2(i):
    print "in func2: " + str(i)  + "\n"
    
func(42, 13, 47, test=17)
func2(43)


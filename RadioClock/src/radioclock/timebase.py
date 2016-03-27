'''
Created on 24.02.2016

@author: hardy
'''
from datetime import datetime
from datetime import timedelta

from kivy.clock import Clock

from swbus import SWBusComponent

TIME_BASE = "TimeBase"
TIME = "Time"
SECOND = "Second"
MINUTE = "Minute"
FIRE = "Fire"
TIMER = "Timer"

INIT = "INIT"
STOP = "STOP"

class TimeBase(SWBusComponent):
    
    timerlist = []
    
    def __init__(self):
        super(TimeBase, self).__init__(TIME_BASE)
        self.run = True
        self.time = datetime.now()
        self.lastminute = datetime.now() - timedelta(minutes=1)
        Clock.schedule_interval(self._check_time, 1)
        
    def register(self):
        self.announce_event(SECOND)
        self.announce_event(MINUTE)
        self.announce_event(FIRE)
        self.define_value(TIME)
        self.define_value(TIMER)
        
    def bus_stop(self):
        self.timerlist=[]
        self.run = False
        
    def get_time(self):
        return self.time
        
    def _check_time(self, dt): 
        self.time = datetime.now()    
        self.raise_event(SECOND, self.time)
        diff = self.time - self.lastminute
        if self.time.second == 0 or diff.seconds >= 60:
            self.lastminute = self.time
            self.raise_event(MINUTE, self.time)
        
        for t in self.timerlist:
            if t.nexttime <= self.time:
                t.count = t.count + 1
                self.raise_event(FIRE, t)
                if t.repeat:
                    t.nexttime = t.nexttime + timedelta(0,t.interval)
                else:
                    self.timerlist.remove(t)
            
        return self.run
    
    def set_timer(self, timer):
        if timer.command == INIT:
            if timer.nexttime is None:
                timer.nexttime = datetime.now() + timedelta(0,timer.interval)
            self.timerlist.append(timer)
        else:
            for t in self.timerlist:
                if t.name == timer.name:
                    self.timerlist.remove(t)
                    break
    
class Timer:
    
    command = ""
    name = ""
    interval = 0
    count = 0
    repeat = False
    nexttime = None
    
    
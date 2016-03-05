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

class TimeBase(SWBusComponent):
    def __init__(self):
        super(TimeBase, self).__init__(TIME_BASE)
        self.run = True
        self.time = datetime.now()
        self.lastminute = datetime.now() - timedelta(minutes=1)
        Clock.schedule_interval(self._check_time, 1)
        
    def register(self):
        self.announce_event(SECOND)
        self.announce_event(MINUTE)
        self.define_value(TIME)
        
    def get_time(self):
        return self.time
        
    def _check_time(self, dt): 
        self.time = datetime.now()    
        self.raise_event(SECOND, self.time)
        diff = self.time - self.lastminute
        if diff.seconds >= 60:
            self.lastminute = self.time
            self.raise_event(MINUTE, self.time)
        return self.run
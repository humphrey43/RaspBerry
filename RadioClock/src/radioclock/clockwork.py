'''
Created on 22.12.2015

@author: hardy
'''

import logger
from player import Source
from swbus import SWBusComponent

CLOCK_WORK = "ClockWork"
TRIGGER = "Trigger"
LED = "LED"
PLAY = "Play"
OFF = "Off"
HALT = "Halt"
DISABLED = "Disabled"
ENABLE = "Enable"
ALARM = "Alarm"
ALARM_TIME = "AlarmTime"
ALARM_INFO = "AlarmInfo"
ALARM_TIME_DISPLAY = "AlarmTimeDisplay"
ALARM_INFO_DISPLAY = "AlarmInfoDisplay"
SOURCE = "Source"
SOURCE_NAME = "SourceName"

class ClockWork(SWBusComponent):
    
    def __init__(self, application):
        super(ClockWork, self).__init__(CLOCK_WORK)
        self.application = application
        self.on = False
        self.disabled = False

    def register(self):
        self.opt_for_event(TRIGGER, self.handle_button)
        self.opt_for_event(HALT, self.handle_halt)
        self.opt_for_event(ALARM, self.handle_alarm)
        self.opt_for_valuechange(ALARM_TIME, self.handle_alarm_time)
        self.opt_for_valuechange(ALARM_INFO, self.handle_alarm_info)
        self.opt_for_valuechange(DISABLED, self.handle_disabled)
        
        self.announce_event(PLAY)
        self.announce_event(OFF)
        self.announce_event(ENABLE)
        
        self.opt_for_value(LED)
        self.opt_for_value(ALARM_TIME_DISPLAY)
        self.opt_for_value(ALARM_INFO_DISPLAY)
        self.opt_for_value(DISABLED)
        self.opt_for_value(SOURCE)
        self.opt_for_value(SOURCE_NAME)
        
    def bus_stop(self):
        self.set_onoff(False)
        self.run = False
    
#############################################################################################
    def handle_button(self, event):
        self.set_onoff(not self.on)
            
    def handle_halt(self, event):
        self.set_onoff(False)
        self.application.system_halt()
            
    def handle_disabled(self, event):
        self.disabled = event.data
            
    def handle_alarm(self, event):
        self.set_value(SOURCE_NAME, "NDR2")
        sound = self.get_value(SOURCE)
        self.raise_event(PLAY, sound)
            
    def handle_alarm_info(self, event):
        self.set_value(ALARM_INFO_DISPLAY, event.data)
            
    def handle_alarm_time(self, event):
        self.set_value(ALARM_TIME_DISPLAY, event.data)
            
    def set_onoff(self, onoff):
        logger.log("set_onoff: " + str(self.on) + str(onoff))
        if self.disabled:
            self.disabled = False
            self.raise_event(ENABLE, True)
        else:
            if self.on and not onoff:
                self.on = False
                self.raise_event(OFF, None)
                self.set_value(LED, self.on)
            elif not self.on and onoff:
                self.on = True
                self.set_value(SOURCE_NAME, "NDR2")
                sound = self.get_value(SOURCE)
                self.raise_event(PLAY, sound)
                self.set_value(LED, self.on)

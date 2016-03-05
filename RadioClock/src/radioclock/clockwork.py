'''
Created on 22.12.2015

@author: hardy
'''

from swbus import SWBusComponent
from player import Source

CLOCK_WORK = "ClockWork"
TRIGGER = "Trigger"
LED = "LED"
PLAY = "Play"
OFF = "Off"
HALT = "Halt"

class ClockWork(SWBusComponent):
    
    def __init__(self, application):
        super(ClockWork, self).__init__(CLOCK_WORK)
        self.application = application
        self.on = False
        self.sound = Source(Source.TYPE_SOURCE_RADIO, "NDR2", "NDR2", "http://ndr-ndr2-nds-mp3.akacast.akamaistream.net/7/400/252763/v1/gnl.akacast.akamaistream.net/ndr_ndr2_nds_mp3.mp3")

    def register(self):
        self.opt_for_event(TRIGGER, self.handle_button)
        self.opt_for_event(HALT, self.handle_halt)
        self.announce_event(PLAY)
        self.announce_event(OFF)
        self.opt_for_value(LED)
        
    def bus_stop(self):
        self.set_onoff(False)
        self.run = False
    
#############################################################################################
    def handle_button(self, event):
        self.set_onoff(not self.on)
            
    def handle_halt(self, event):
        self.set_onoff(False)
        self.application.system_halt()
            
    def set_onoff(self, onoff):
        if self.on and not onoff:
            self.on = False
            self.raise_event(OFF, None)
            self.set_value(LED, self.on)
        elif not self.on and onoff:
            self.on = True
            self.raise_event(PLAY, self.sound)
            self.set_value(LED, self.on)

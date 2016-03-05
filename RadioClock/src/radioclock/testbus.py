'''
Created on 19.02.2016

@author: hardy
'''
import time
import swbus
from swbus import SWBusComponent
from timebase import TimeBase
from player import Player, Source
from clockwork import ClockWork
from environment import Environment

class HandleEvent:
    def __init__(self, eventname):
        self.eventname = eventname
        
    def __call__(self, func):
        swbus.master.register_for_event(self.eventname, func)
        return func
    
class Comp1(SWBusComponent):
    def __init__(self):
        super(Comp1, self).__init__("Comp1")

    def register(self):
        self.opt_for_event( "Time", self._handle_time)
        self.opt_for_event( "Event1", self._handle_event1)
        self.opt_for_valuechange("Value1", self._handle_value1change)
        self.opt_for_value("Value2")
        self.opt_for_value("Value3")

#    @HandleEvent("Test.Comp2.Event1")
    def _handle_event1(self, event):
        print event.data
      
    def _handle_time(self, event):
        print event.data
      
    def _handle_value1change(self, event):
        print event.eventname + ": " + str(event.data)
      
class Comp2(SWBusComponent):

    def __init__(self):
        super(Comp2, self).__init__("Comp2")
        self.value2 = "value2_0"
        self.value3 = "value3_0"
        
    def register(self):
        self.announce_event("Event1")
        self.define_value("Value1", valuechange=True)
        self.define_value("Value2")
        self.define_value("Value3")
        
    def sendEvent(self):
        self.raise_event("Event1", "Hallo Welt")

    def sendValueChange(self):
        self.raise_valuechange("Value1", 42)

    def set_value3(self, value):
        self.value2 = value

    def get_value2(self):
        return self.value2
    
            
tb = swbus.master.register_component(TimeBase())
comp1 = swbus.master.register_component(Comp1())
comp2 = swbus.master.register_component(Comp2())
p = swbus.master.register_component(Player())
env = swbus.master.register_component(Environment())
clockWork = swbus.master.register_component(ClockWork())

swbus.connect_components(
    '''
    TimeBase.Second -> ClockFace.Volume
    Comp2.Event1 -> Comp1.Event1
    Comp2.Value1 -> Comp1.Value1
    Comp2.Value2 -> Comp1.Value2
    Comp2.Value3 -> Comp1.Value3

# dies ist ein Kommentar
    Environment.Button1LED -> ClockWork.LED 
    Environment.Button1    -> ClockWork.Trigger
    ClockWork.Play         -> Player.Play
    ClockWork.Off          -> Player.Off
     
    ''')
#swbus.master.bind_event(tb, timebase.SECOND, comp1, "Time")
#swbus.master.bind_event(comp2, "Event1", comp1, "Event1")
#swbus.master.bind_valuechange(comp2, "Value1", comp1, "Value1")
#swbus.master.bind_value(comp2, "Value2", comp1, "Value2")
#swbus.master.bind_value(comp2, "Value3", comp1, "Value3")


s = Source(Source.TYPE_SOURCE_RADIO, "NDR2", "NDR2", "http://ndr-ndr2-nds-mp3.akacast.akamaistream.net/7/400/252763/v1/gnl.akacast.akamaistream.net/ndr_ndr2_nds_mp3.mp3")
p.play(s)

comp2.sendEvent()
swbus.master._work_events(1)
comp2.sendValueChange()
swbus.master._work_events(2)
print "Value2: " + str(comp1.get_value("Value2"))
comp1.set_value("Value3", "TestV 3")
p.stop()
print "Value2: " + str(comp1.get_value("Value2"))
env.push_button1()
while True:
    time.sleep(5)
swbus.master._work_events(2)
swbus.master._work_events(3)
swbus.master._work_events(4)
#env.push_button1()
#swbus.master._work_events(2)
#p.start()
#p.off()
swbus.master.bus_stop()
i = 42

    
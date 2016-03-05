from kivy.clock import Clock
from Queue import Queue
from EventInfo import EventInfo
from Listener import Listener

class SWBusMaster:

    def __init__(self):
        self.components = {}
        self.events = {}
        self.values = {}
        self.event_queue = Queue()

#       start the event handler loop
        self.run = True
        Clock.schedule_interval(self._work_events, 1)
    
    def _work_events(self):
#        print "work_events" + str(data)
        while not self.event_queue.empty():
            event = self.event_queue.get(False)
            if event is not None:
                if self.events.has_key(event.eventname):
                    eventinfo = self.events[event.eventname]
                    for listener in eventinfo.listeners:
                        listener.callback(event)
        return self.run

    def stop(self):
        self.run = False
        
    def raise_event(self, event):
        self.event_queue.put(event)

    def set_value(self, name, data):
        pass

    def getValue(self, name):
        pass
    
    def register_component(self, component):
        self.components[component.fullname] = component
        component.register()
        
    def register_for_event(self, component, eventname, callback):
        if not self.events.has_key(eventname):
            eventinfo = EventInfo(eventname)
            self.events[eventname] = eventinfo
        else:
            eventinfo = self.events[eventname]
        eventinfo.add_listener(Listener(component, callback))

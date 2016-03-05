'''
Created on 18.02.2016

@author: hardy
'''
from kivy.clock import Clock
from Queue import Queue

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

        
'''
def register_component(component):
    components[component.fullname] = component
    component.register()

def unregister_component(component):
    if components.has_key(component.fullname):
        del components[component.fullname]
        for event in events:
            pass
        for value in values:
            pass
            
def register_for_event(eventname, name, callback):
    if not events.has_key(eventname):
         = event
    pass

def unregister_for_Event(name):
    pass


'''
        
class SWBusComponent:

    def handle_event(self, name, data):
        pass

    def set_value(self, name, data):
        pass

    def getValue(self, name):
        pass


class Event:
    def __init__(self, component, eventname, data=None):
        self.component = component
        self.eventname = eventname
        self.data = data

class EventInfo:
    def __init__(self, eventname):
        self.eventname = eventname
        self.listeners = []
        
    def add_listener(self, listener):
        self.listeners.append(listener)

class Listener:
    def __init__(self, component, callback):
        self.component = component
        self.callback = callback

        

        
class ValueInfo:
    pass

master = SWBusMaster() # Singleton


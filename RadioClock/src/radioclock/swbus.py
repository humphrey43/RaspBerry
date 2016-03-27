'''
Created on 18.02.2016

@author: hardy
'''
from kivy.clock import Clock
from kivy.graphics import Color
from Queue import Queue

READ = "R"
WRITE = "W"
READ_WRITE = "RW"


class SWBusMaster:

    def __init__(self):
        self.components = {}
        self.events = {}
        self.values = {}
        self.event_queue = Queue()

#       start the event handler loop
        self.run = True
        Clock.schedule_interval(self._work_events, 0.5)

    def read_configurations(self, config):    
        for component in self.components.itervalues():
            component.read_configuration(config)

    def bus_stop(self):    
        for component in self.components.itervalues():
            component.bus_stop()
        self.run = False
        
#############################################################################################
    def _work_events(self, data):
#        print "work_events " + str(data)
        while not self.event_queue.empty():
            event = self.event_queue.get(False)
            if event is not None:
                if self.events.has_key(event.eventname):
                    eventinfo = self.events[event.eventname]
                    for listener in eventinfo.listeners:
                        listener.callback(event)
        return self.run

#############################################################################################
    def raise_event(self, event):
        self.event_queue.put(event)

    def raise_valuechange(self, valuename, value):
        event = Event(valuename, value)
        self.event_queue.put(event)

    def set_value(self, valuename, data):
        valueinfo = self.values[valuename]
        if valueinfo is not None:
            if 'W' in valueinfo.accesstype:
                valueinfo.component.set_own_value(valueinfo.valuename, data)

    def get_value(self, valuename):
        value = None
        valueinfo = self.values[valuename]
        if valueinfo is not None:
            if 'R' in valueinfo.accesstype:
                value = valueinfo.component.get_own_value(valueinfo.valuename)
        return value
    
#############################################################################################
    def register_component(self, component):
        self.components[component.name] = component
        component.register()
        return component
        
    def get_component(self, name):
        component = None
        try:
            component = self.components[name]
        except:
            pass
        return component
        
    def register_for_event(self, eventname, callback):
        if not self.events.has_key(eventname):
            eventinfo = EventInfo(eventname)
            self.events[eventname] = eventinfo
        else:
            eventinfo = self.events[eventname]
        eventinfo.add_listener(Listener(callback))

    def register_for_valuechange(self, valuename, callback):
        if not self.events.has_key(valuename):
            eventinfo = EventInfo(valuename)
            self.events[valuename] = eventinfo
        else:
            eventinfo = self.events[valuename]
        eventinfo.add_listener(Listener(callback))

    def register_value(self, component, valuename, accesstype):
        if not self.values.has_key(valuename):
            valueinfo = ValueInfo(valuename)
            self.values[valuename] = valueinfo
        else:
            valueinfo = self.values[valuename]
        valueinfo.valuename = valuename
        valueinfo.component = component
        valueinfo.accesstype = accesstype.upper()

    def bind(self, comp_from, name_from, comp_to, name_to):
        event_from = check_event_from(comp_from, name_from)
        event_to = check_event_to(comp_to, name_to)
        valuechange_from = check_valuechange_from(comp_from, name_from)
        valuechange_to = check_valuechange_to(comp_to, name_to)
        value_from = check_value_from(comp_from, name_from)
        value_to = check_value_to(comp_to, name_to)
    
        found = False
        if event_from is not None and event_to is not None:
            self.register_for_event(comp_from.name + "." + name_from, event_to.callback)
            print "event " + comp_from.name + "." + name_from + " connected to " + comp_to.name + "." + name_to
            found = True
            
        if valuechange_from is not None and valuechange_to is not None:
            self.register_for_valuechange(comp_from.name + "." + name_from, valuechange_to.callback)
            print "valuechange " + comp_from.name + "." + name_from + " connected to " + comp_to.name + "." + name_to
            found = True
            
        if value_from is not None and value_to is not None:
            value_to.fullname = comp_from.name + "." + name_from
            print "value " + comp_from.name + "." + name_from + " connected to " + comp_to.name + "." + name_to
            found = True
        
        if not found:
            print "-- connection not possible: " + comp_from.name + "." + name_from + " --> " + comp_to.name + "." + name_to + " ---------------"
            if event_from is not None:
                print comp_from.name + " has event " + name_from
            if valuechange_from is not None:
                print comp_from.name + " has valuechange " + name_from
            if value_from is not None:
                print comp_from.name + " has value " + name_from
            if event_to is not None:
                print comp_to.name + " has event " + name_to
            if valuechange_to is not None:
                print comp_to.name + " has valuechange " + name_to
            if value_to is not None:
                print comp_to.name + " has value " + name_to

'''    def bind_event(self, comp_from, name_from, comp_to, name_to):
        event_from = comp_from.announced_events[name_from]
        event_to = comp_to.opt_events[name_to]
        if event_from is not None and event_to is not None:
            self.register_for_event(comp_from.name + "." + name_from, event_to.callback)
    
    def bind_valuechange(self, comp_from, name_from, comp_to, name_to):
        event_from = comp_from.announced_valuechanges[name_from]
        event_to = comp_to.opt_valuechanges[name_to]
        if event_from is not None and event_to is not None:
            self.register_for_valuechange(comp_from.name + "." + name_from, event_to.callback)

    def bind_value(self, comp_from, name_from, comp_to, name_to):
        value_from = self.values[comp_from.name + "." + name_from]
        value_to = comp_to.opt_values[name_to]
        if value_from is not None and value_to is not None:
            value_to.fullname = comp_from.name + "." + name_from

        
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
        
class SWBusComponent(object):
    
    def __init__(self, name):
        self.name = name
        self.config = None
        self.run = True
        self.in_init = True
        self.values = {}
        self.opt_events = {}
        self.opt_valuechanges = {}
        self.opt_values = {}
        self.announced_events = {}
        self.announced_valuechanges = {}
        
    def register(self):
        pass
    
    def bus_stop(self):
        self.run = False
    
    def handle_event(self, event):
        pass

    def register_for_event(self, eventname, callback):
        global master
        master.register_for_event(eventname, callback)

    def opt_for_event(self, eventname, callback):
        info = OptEventInfo(eventname, callback)
        self.opt_events[eventname] = info

    def announce_event(self, eventname):
        info = OptEventInfo(eventname, None)
        self.announced_events[eventname] = info

    def opt_for_valuechange(self, valuename, callback):
        info = OptEventInfo(valuename, callback)
        self.opt_valuechanges[valuename] = info

    def register_for_valuechange(self, valuename, callback):
        global master
        master.register_for_valuechange(valuename, callback)

    def opt_for_value(self, valuename):
        info = OptValueInfo(valuename)
        self.opt_values[valuename] = info

    def announce_valuechange(self, valuename):
        info = OptEventInfo(valuename, None)
        self.announced_valuechanges[valuename] = info

    def register_value(self, valuename, accesstype):
        global master
        fullname = self.name + "." + valuename
        master.register_value(self, fullname, accesstype)

        
#############################################################################################
    def set_value(self, valuename, data):
        info = self.opt_values[valuename]
        if info is not None and info.fullname is not None:
            master.set_value(info.fullname, data)

    def get_value(self, valuename):
        value = None
        info = self.opt_values[valuename]
        if info is not None and info.fullname is not None:
            value = master.get_value(info.fullname)
        return value
        
    def set_own_value(self, valuename, data):
        name = self.normalize(valuename)
        info = self.values[name]
        if info is not None:
            info.set_value(valuename, data)

    def get_own_value(self, valuename):
        value = None
        name = self.normalize(valuename)
        info = self.values[name]
        if info is not None:
            value = info.get_value(valuename)
        return value
        
    def normalize(self, fullname):
        parts = fullname.split(".")
        name = parts.pop()
        return name
        
    def raise_event(self, eventname, data):
        global master
        event = Event(self.name + "." + eventname, data)
        if eventname <> "Second":
            print "Event: " + event.eventname 
        master.raise_event(event)

    def raise_valuechange(self, valuename, value):
        global master
        fullname = self.name + "." + valuename
        master.raise_valuechange(fullname, value)

    def read_configuration(self, config):
        self.config = config
        self.in_init = False
        
    def save_configuration(self):
        if not self.in_init:
            self.config.write()
        
    def set_config(self, valuename, value):
        self.config.set(self.name, valuename.lower(), value)
        self.save_configuration()

    def get_config_int(self, valuename):
        return self.config.getint(self.name, valuename.lower())

    def get_config_value(self, valuename):
        return self.config.get(self.name, valuename.lower())

    def get_config_color(self, valuename):
        r = self.get_config_int(valuename + "_r") / 256.0
        g = self.get_config_int(valuename + "_g") / 256.0
        b = self.get_config_int(valuename + "_b") / 256.0
        return Color(r, g, b, 1)

    def get_config_color_list(self, valuename):
        r = self.get_config_int(valuename + "_r") / 256.0
        g = self.get_config_int(valuename + "_g") / 256.0
        b = self.get_config_int(valuename + "_b") / 256.0
        return [r, g, b, 1]

    def define_value(self, valuename, register = True, setter=None, getter=None, valuechange=False):
        info = LocalValueInfo(self, valuename, register, setter, getter)
        self.values[valuename] = info
        if valuechange:
            self.announce_valuechange(valuename)

class Event(object):
    def __init__(self, eventname, data=None):
#        self.component = component
        self.eventname = eventname
        self.data = data

class OptEventInfo(object):
    def __init__(self, eventname, callback):
        self.eventname = eventname
        self.callback = callback
        
class EventInfo(object):
    def __init__(self, eventname):
        self.eventname = eventname
        self.listeners = []
        
    def add_listener(self, listener):
        self.listeners.append(listener)

class Listener(object):
    def __init__(self, callback):
#        self.component = component
        self.callback = callback
#    def __init__(self, component, callback):
#        self.component = component
#        self.callback = callback

        

        
class ValueInfo(object):
    def __init__(self, valuename):
        self.valuename = valuename
        self.component = None
        self.accesstype = ""
        
class OptValueInfo(object):
    def __init__(self, valuename):
        self.valuename = valuename
        self.fullname = None

class LocalValueInfo(object):
    def __init__(self, component, valuename, register = True, setter=None, getter=None):
        self.valuename = valuename
        self.component = component
        self.setter = self.find_method("set", setter)
        self.getter = self.find_method("get", getter)
        accesstype = ""
        if self.getter is not None:
            accesstype = READ
        if self.setter is not None:
            accesstype = accesstype + WRITE
        component.register_value(valuename, accesstype)
        
    
    def find_method(self, accesstype, defaultvalue):
        method = None
        if defaultvalue is None:
            name = accesstype + "_" + self.valuename.lower()
            try:
                if hasattr(self.component, name) and callable(getattr(self.component, name)):
                    method = getattr(self.component, name)
            except:
                pass
        else:
            if callable(defaultvalue):
                method = defaultvalue
        return method
    
    def set_value(self, valuename, value):
        if self.setter is not None:
            self.setter(value)
        
    def get_value(self, valuename):
        value = None
        if self.getter is not None:
            value = self.getter()
        return value
    
def check_event_from(comp, name):
    return check_defined(comp.announced_events, name)

def check_event_to(comp, name):
    return check_defined(comp.opt_events, name)

def check_valuechange_from(comp, name):
    return check_defined(comp.announced_valuechanges, name)

def check_valuechange_to(comp, name):
    return check_defined(comp.opt_valuechanges, name)

def check_value_from(comp, name):
    return check_defined(comp.values, name)

def check_value_to(comp, name):
    return check_defined(comp.opt_values, name)

def check_defined(objects, name):   
    obj = None
    try:
        obj = objects[name]
    except:
        pass
    return obj

def connect_components(wiring):
    connections = wiring.split("\n")
    for connection in connections: 
        c = connection.strip()
        if c <> "\n" and c <> "" and c[0] <> '#':
            from_to = c.split("->")
            comp_name_from = from_to[0].strip().split(".")
            comp_name_to = from_to[1].strip().split(".")
            comp_from = master.get_component(comp_name_from[0])
            if comp_from is None:
                print " component " + comp_name_from[0] + " is  unknown"
            comp_to = master.get_component(comp_name_to[0])
            if comp_to is None:
                print " component " + comp_name_to[0] + " is  unknown"
            if comp_from is not None and comp_to is not None:
                master.bind(comp_from, comp_name_from[1], comp_to, comp_name_to[1])
 
master = SWBusMaster() # Singleton


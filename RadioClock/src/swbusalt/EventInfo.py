class EventInfo:
    def __init__(self, eventname):
        self.eventname = eventname
        self.listeners = []
        
    def add_listener(self, listener):
        self.listeners.append(listener)

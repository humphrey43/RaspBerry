class Event:
    def __init__(self, component, eventname, data=None):
        self.component = component
        self.eventname = eventname
        self.data = data

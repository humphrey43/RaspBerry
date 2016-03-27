'''
Created on 27.02.2016

@author: hardy
'''

class EnvironmentTest(object):

    def __init__(self):
        self.nextambientlight = 0
        self.handler = None        
        
    def stop(self):
        pass
    
#############################################################################################
        
    def set_handler(self, handler):
        self.handler = handler
        
    def set_volume(self, volume):
        print "set_volume: " + str(volume)

    def set_brightness(self, brightness):
        print "set_brightness: " + str(brightness)

    def set_button1_led(self, on_off):
        print "set_button1_led: " + str(on_off)

    def get_ambient_light(self):
        return self.nextambientlight

#############################################################################################
# methods for test
#############################################################################################
    def set_ambient_light(self, value):
        self.nextambientlight = value

    def push_button1(self):
        self.handler.handle_button1()

    def log_ambient_light(self):
        pass

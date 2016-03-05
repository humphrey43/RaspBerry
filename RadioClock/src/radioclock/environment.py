'''
Created on 27.02.2016

@author: hardy
'''
from kivy.clock import Clock

from swbus import SWBusComponent
import classes

ENVIRONMENT = "Environment"
VOLUME = "Volume"
BRIGHTNESS = "Brightness"
AMBIENT_LIGHT = "AmbientLight"
BUTTON1 = "Button1"
BUTTON1_LED = "Button1LED"

class Environment(SWBusComponent):

#############################################################################################
#
#   Initialize of Class
#
#############################################################################################
    def __init__(self):
        super(Environment, self).__init__(ENVIRONMENT)
        
        self.ambientlight = 0
        self.realenvironment = classes.get_instance_of_class("environment_test.EnvironmentTest")
        Clock.schedule_interval(self._check_ambient, 2)
                
    def register(self):
        self.opt_for_valuechange(VOLUME, self._set_volume)
        self.opt_for_valuechange(BRIGHTNESS, self._set_brightness)
        
        self.announce_event(BUTTON1)
        
        self.define_value(VOLUME)
        self.define_value(BRIGHTNESS)
        self.define_value(AMBIENT_LIGHT, valuechange=True)
        self.define_value(BUTTON1_LED)
        
    def bus_stop(self):
        self.realenvironment.stop()
        self.run = False
    
    def read_configuration(self, config):
        self.config = config
        self.realenvironment = classes.get_instance_of_class(self.get_config_value("RealClass"))
        self.realenvironment.set_handler(self)
        self.in_init = False
        
#############################################################################################
    def set_volume(self, volume):
        self.realenvironment.set_volume(volume)

    def set_brightness(self, brightness):
        self.realenvironment.set_brightness(brightness)

    def set_button1led(self, on_off):
        self.realenvironment.set_button1_led(on_off)

    def handle_button1(self, channel):
        self.raise_event(BUTTON1, None)

    def push_button1(self):
        self.raise_event(BUTTON1, None)

    def get_ambientlight(self):
        return self.ambientlight
        
    def _check_ambient(self, dt): 
        if not self.in_init:
            al = self.realenvironment.get_ambient_light()
            if self.ambientlight <> al:
                self.ambientlight = al
                self.raise_valuechange(AMBIENT_LIGHT, self.ambientlight)
        return self.run
    
#############################################################################################
    def _set_volume(self, volume):
        pass

    def _set_brightness(self, brightness):
        pass


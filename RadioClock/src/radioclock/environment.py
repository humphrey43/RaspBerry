'''
Created on 27.02.2016

@author: hardy
'''
import os

from kivy.clock import Clock

from swbus import SWBusComponent
import classes

ENVIRONMENT = "Environment"
VOLUME = "Volume"
BRIGHTNESS = "Brightness"
AMBIENT_LIGHT = "AmbientLight"
BUTTON1 = "Button1"
BUTTON1_LED = "Button1LED"
TIME = "Time"
OS_NAME = "OSName"

class Environment(SWBusComponent):

#############################################################################################
#
#   Initialize of Class
#
#############################################################################################
    def __init__(self):
        super(Environment, self).__init__(ENVIRONMENT)
        
        self.ambientlight = {'c':0,'r':0,'g':0,'b':0,'l':0}
        self.ambientstring = self.ambient_to_string(self.ambientlight)
        self.realenvironment = classes.get_instance_of_class("environment_test.EnvironmentTest")
        Clock.schedule_interval(self._check_ambient, 2)
                
    def register(self):
        self.opt_for_event(TIME, self._handle_time)
        self.opt_for_valuechange(VOLUME, self._set_volume)
        self.opt_for_valuechange(BRIGHTNESS, self._set_brightness)
        
        self.announce_event(BUTTON1)
        
        self.define_value(VOLUME)
        self.define_value(BRIGHTNESS)
        self.define_value(AMBIENT_LIGHT, valuechange=True)
        self.define_value(BUTTON1_LED)
        self.define_value(OS_NAME)
        
    def bus_stop(self):
        self.realenvironment.stop()
        self.run = False
    
    def read_configuration(self, config):
        self.config = config

        print os.name
        envtype = self.get_config_value("EnvironmentType")
        self.os_name = os.name
        
        classname = "environment_test.EnvironmentTest"
        if (envtype == "os"):
            if os.name == "nt":
                classname = "environment_windows.EnvironmentWindows"
            elif os.name == "posix":
                classname = "environment_pi.EnvironmentPi"
                
        self.realenvironment = classes.get_instance_of_class(classname)
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
        
    def ambient_to_string(self, al): 
        crgbl = "C: %s, R: %s, G: %s, B: %s, L: %s\n" % (al['c'], al['r'], al['g'], al['b'], al['l'])
        return crgbl

    def _check_ambient(self, dt): 
        if not self.in_init:
            al = self.realenvironment.get_ambient_light()
            crgbl = self.ambient_to_string(al)
            if self.ambientstring <> crgbl:
                self.ambientlight = al
                self.ambientstring = crgbl
                self.raise_valuechange(AMBIENT_LIGHT, self.ambientlight)
        return self.run

    def _check_ambient2(self, dt): 
        if not self.in_init:
            al = self.realenvironment.get_ambient_light()
            if self.ambientlight <> al:
                self.ambientlight = al
                self.raise_valuechange(AMBIENT_LIGHT, self.ambientlight)
        return self.run

    def _handle_time(self, event):
        self.realenvironment.log_ambient_light(self.ambientstring)
        if os.name == 'nt':
            self.raise_valuechange(AMBIENT_LIGHT, self.ambientlight)
        
    
#############################################################################################
    def _set_volume(self, volume):
        self.set_volume(volume.data)

    def _set_brightness(self, brightness):
        self.set_brightness(brightness.data)

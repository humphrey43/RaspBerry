'''
Created on 15.02.2016

@author: hardy
'''

from datetime import datetime
import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics import Color
from kivy.graphics import Rectangle
from swbus import SWBusComponent

kivy.require('1.0.7')

CLOCK_FACE = "ClockFace"
TIME = "Time"
AMBIENT_LIGHT = "AmbientLight"
VOLUME = "Volume"
BRIGHTNESS = "Brightness"
BRIGHTNESS_LOW = "BrightnessLow"
BRIGHTNESS_HIGH = "BrightnessHigh"
ALARM_INFO = "AlarmInfo"
ALARM_TIME = "AlarmTime"
NIGHT_TIME = "NightTime"

STOP = "Stop"

THRESHOLD1 = "Threshold1"
THRESHOLD2 = "Threshold2"

    
#############################################################################################
class ClockFace(SWBusComponent):
    
#############################################################################################
    def __init__(self):
        super(ClockFace, self).__init__(CLOCK_FACE)
        self.visible = False
        self.nighttime = False

        self.brightness_high = 100
        self.threshold1 = 70
        self.threshold2 = 10
        self.brightness_low = 20
        self.last_brightness = -1
        self.last_volume = -1

#############################################################################################
#
#   Methods for SWBusComponent
#
#############################################################################################
    def register(self):
        self.opt_for_event(TIME, self._handle_second)
        self.opt_for_valuechange(AMBIENT_LIGHT, self._handle_ambientlight)
        
        self.announce_event(STOP)
        
        self.announce_valuechange(VOLUME)
        self.announce_valuechange(BRIGHTNESS)
        self.announce_valuechange(NIGHT_TIME)
        
        self.define_value(VOLUME)
        self.define_value(BRIGHTNESS)
        self.define_value(ALARM_INFO)
        self.define_value(ALARM_TIME)
        self.define_value(NIGHT_TIME)
        
    def read_configuration(self, config):
        self.config = config

        self.set_volume(self.get_config_int(VOLUME))
        self.brightness_high = self.get_config_int(BRIGHTNESS_HIGH)
        self.threshold1 = self.get_config_int(THRESHOLD1)
        self.threshold2 = self.get_config_int(THRESHOLD2)
        self.brightness_low = self.get_config_int(BRIGHTNESS_LOW)
        if self.nighttime:
            self.set_brightness(self.brightness_low)
        else:
            self.set_brightness(self.brightness_high)
        self.in_init = False
        
#############################################################################################
    def build(self):

        tw1 = 60
        tw = 800 - 2 * tw1
        th1 = 60
        th = 480 - 2 * th1
        
        aw1 = 100
        aw = tw - 2 * aw1
        
        layout1 = GridLayout(rows=3,cols=3,
                             cols_minimum= {0:tw1, 1:tw, 2:tw1},
                             col_force_default= True,
                             rows_minimum= {0:th1, 1:th, 2:th1},
                             row_force_default= True)
        
        self.widget1_1 = self._add_widget(layout1, Label(text="1,1"), "", Color(0, 0, 0))
        self._set_visibility_control(self.widget1_1, False)

        layout2 = GridLayout(cols=3,
                             cols_minimum= {0:aw1, 1:aw, 2:aw1},
                             col_force_default= True)
        
        self.button_alarmtime = self._add_widget(layout2, Button(text="22:30", size_hint=(.8, .8), background_color=[0, 0, 0], background_normal = ''), "", Color(0, 0, 0))
        self.button_alarmtime.font_size='32dp'
        self.button_alarminfo = self._add_widget(layout2, Button(text="Radio NDR2", size_hint=(.8, .8), background_color=[0, 0, 0], background_normal = ''), "", Color(0, 0, 0))
        self.button_alarminfo.font_size='32dp'
        self.label_volume = self._add_widget(layout2, Label(text="100"), "", Color(0, 0, 0))
        self.label_volume.font_size='32dp'
        layout1.add_widget(layout2)
        
        self.button_on = self._add_widget(layout1, Button(text="an", on_press=self.switch_on, size_hint=(.8, .8)), "", Color(0, 0, 0))
        
        self.brightslider = self._add_widget(layout1, Slider(min=0, max = 100, value = 25, size_hint=(.05, .8), orientation='vertical', step=1), "", Color(0, 0, 0))
        self.brightslider.bind(value=self._brightness_changed)
        
        self.time = self._add_widget(layout1, Label(text=datetime.now().isoformat()[11:19]), "", Color(0, 0, 0))
        self.time.font_size='128dp'

        self.volslider = self._add_widget(layout1, Slider(min=0, max = 100, value = 25, size_hint=(.05, .8), orientation='vertical', step=1), "", Color(0, 0, 0))
        self.volslider.bind(value=self._volume_changed)
        
        self.button_stop = self._add_widget(layout1, Button(text="Stop", on_press=self.switch_stop, size_hint=(.8, .8)), "", Color(0, 0, 0))
#        self._set_visibility_control(self.widget3_1, False)
        
        self.widget3_2 = self._add_widget(layout1, Label(text="3,2"), "", Color(0, 0, 0))
        self._set_visibility_control(self.widget3_2, False)

        self.button_off = self._add_widget(layout1, Button(text="aus", on_press=self.switch_off, size_hint=(.8, .8)), "", Color(0, 0, 0))

        self.set_visible(self.visible)
#        self.set_volume(50)    

        return layout1


#############################################################################################
    def get_visible(self):
        return self.visible
    
    def set_visible(self, visible):
        self._set_visibility_control(self.brightslider, visible)
        self._set_visibility_control(self.volslider, visible)
        self._set_visibility_control(self.button_on, visible)
        self._set_visibility_control(self.button_off, visible)
        self._set_visibility_control(self.button_stop, visible)
#        self._set_visibility_control(self.button_alarminfo, visible)
        self._visible = visible

#############################################################################################
    def _handle_second(self, event):
        self.set_time(event.data)
        
    def set_time(self, time):
        self.time.text = time.isoformat()[11:19]
                
#############################################################################################
    def set_alarminfo(self, info):
        self.button_alarminfo.text = info
        
    def get_alarminfo(self):
        return self.button_alarminfo.text
        
#############################################################################################
    def set_alarmtime(self, info):
        self.button_alarmtime.text = info
        
    def get_alarmtime(self):
        return self.button_alarmtime.text
        
#############################################################################################
    def switch_on(self, instance):
        self.set_visible(True)

    def switch_off(self, instance):
        self.set_visible(False)

    def switch_stop(self, instance):
        self.raise_event(STOP, None)

        
#############################################################################################
#    def set_volume_changed(self, method, obj=None):
#        self.callback_off = classes.CallbackInfo(method)
        
    def set_volume(self, value):
        print VOLUME, value
        valueint = int(value)
        if self.last_volume <> value:
            self.last_volume = value
            self.volslider.value = value
            self.label_volume.text = str(valueint)
            self.raise_valuechange(VOLUME, valueint)
            self.set_config(VOLUME, valueint)
            
    def get_volume(self):
        return self.last_volume

    def _volume_changed(self, instance, value):
        self.set_volume(value)

#############################################################################################
#    def set_brightness_changed(self, method, obj=None):
#        self.callback_brightness = classes.CallbackInfo(method)
        
    def set_brightness(self, value):
        print BRIGHTNESS, value
        valueint = int(value)
        if self.last_brightness <> value:
            self.last_brightness = value
            self.brightslider.value = value
            self.raise_valuechange(BRIGHTNESS, valueint)
            if self.nighttime:
                self.set_config(BRIGHTNESS_LOW, valueint)
            else:
                self.set_config(BRIGHTNESS_HIGH, valueint)
        
    def get_brightness(self):
        return self.last_brightness

    def _brightness_changed(self, instance, value):
        self.set_brightness(value)
        
    def _handle_ambientlight(self, event):
        print event.eventname + ": " + str(event.data)
        
#############################################################################################
    def set_outside_brightness(self, value):
        self.outside_brightness = value

#############################################################################################
    def set_nighttime(self, value):
        if self.nighttime <> value:
            self.nighttime = value
            self.raise_valuechange(NIGHT_TIME, value)

    def get_nighttime(self):
        return self.nighttime

       
#############################################################################################
#
#  internal methods
#
#############################################################################################

    def _add_widget(self, layout, widget, widget_id, background=Color(0, 0, 0)):
        self._add_background(widget, background)
        if widget_id != "":
            widget.id = widget_id
        layout.add_widget(widget)
        return widget
    
    def _update_rect(self, widget, value):
        widget.rect.pos = widget.pos
        widget.rect.size = widget.size
        if widget.__dict__["rect2"] is not None:
            widget.rect2.pos = widget.pos
            widget.rect2.size = widget.size
    
    def _add_background(self, widget, background):
        widget.rect = Rectangle(pos=widget.pos, size=widget.size)
        widget.canvas.before.add(background)
        widget.canvas.before.add(widget.rect)
        widget.bind(pos=self._update_rect, size=self._update_rect)
        
        widget.rect2 = Rectangle(pos=widget.pos, size=widget.size)
        widget.color2 = Color(0,0,0,0)
        widget.canvas.after.add(widget.color2)
        widget.canvas.after.add(widget.rect2)
        
    def _set_visibility_control(self, widget, visible):
        if widget.__dict__["color2"] is not None:
            if visible:
                widget.color2.a = 0
            else:
                widget.color2.a = 1

#    def _brightness_changed(self, instance, value):
#        print "Brightness", value
#        if self.callback_brightness is not None:
#            self.callback_brightness.call(instance, value)


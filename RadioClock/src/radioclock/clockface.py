'''
Created on 15.02.2016

@author: hardy
'''
import os
from datetime import datetime

import kivy
from kivy.uix.layout import Layout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics import Color
from kivy.graphics import Rectangle

from swbus import SWBusComponent, Event
import logger

kivy.require('1.0.7')

CLOCK_FACE = "ClockFace"
TIME = "Time"
AMBIENT_LIGHT = "AmbientLight"
VOLUME = "Volume"
VOLUME_50 = "Volume50"
BRIGHTNESS = "Brightness"
BRIGHTNESS_LOW = "BrightnessLow"
BRIGHTNESS_HIGH = "BrightnessHigh"
BRIGHTNESS_50 = "Brightness50"
RGB_LOW = "RGBLow"
COLOR = "Color"
ALARM_INFO = "AlarmInfo"
ALARM_TIME = "AlarmTime"
NIGHT_TIME = "NightTime"
DIGITS = "Digits"
STOP = "Stop"
CLEAN = "Clean"
ENABLE = "Enable"
CLICK = "Click"
BACKGROUND_DAY = "BackgroundDay"
FOREGROUND_DAY = "ForegroundDay"
BACKGROUND_NIGHT = "BackgroundNight"
FOREGROUND_NIGHT = "ForegroundNight"

THRESHOLD1 = "Threshold1"
THRESHOLD2 = "Threshold2"

    
#############################################################################################
class ClockFace(SWBusComponent):
    
#############################################################################################
    def __init__(self):
        super(ClockFace, self).__init__(CLOCK_FACE)
        self.digits = 4
        self.last_time_pos = 16
        
        self.visible = False

        self.adaptor_volume = ValueAdaptor([[0.5, 0.7]], [[0, 100], [0, 100]])
        self.last_volume = -1

        self.adaptor_brightness = ValueAdaptor([[0.3, 0.7],[0.6, 0.9]], [[0, 100], [0, 100]])
        self.nighttime = 0
        self.brightness_low = 20
        self.brightness_high = 100
        self.brightness = [100, 20]
        self.threshold1 = 70
        self.threshold2 = 10
        self.ambient_day = {'c':318,'r':200,'g':200,'b':200,'l':100}
        self.ambient_night = {'c':50,'r':200,'g':200,'b':200,'l':100}
        self.ambient_night2 = {'c':5,'r':200,'g':200,'b':200,'l':100}
        self.ambient_light = self.ambient_day
        self.last_brightness = -1
        self.actual_brightness = 100
        self.user_change = True
        
        self.clean = False;

#############################################################################################
#
#   Methods for SWBusComponent
#
#############################################################################################
    def register(self):
        self.opt_for_event(TIME, self._handle_time)
        self.opt_for_event(ENABLE, self._handle_enable)
        self.opt_for_valuechange(AMBIENT_LIGHT, self._handle_ambientlight)
        
        self.announce_event(STOP)
        self.announce_event(CLICK)
        
        self.define_value(VOLUME, valuechange=True)
        self.define_value(BRIGHTNESS, valuechange=True)
        self.define_value(ALARM_INFO)
        self.define_value(ALARM_TIME)
        self.define_value(NIGHT_TIME, valuechange=True)
        self.define_value(CLEAN, valuechange=True)
        
    def read_configuration1(self, config):
        self.config = config

        self.digits = self.get_config_int(DIGITS)
        if self.digits == 6:    
            self.last_time_pos = 19
            
        self.background_day = self.get_config_color(BACKGROUND_DAY)
        self.foreground_day = self.get_config_color(FOREGROUND_DAY)
        self.background_night = self.get_config_color(BACKGROUND_NIGHT)
        self.foreground_night = self.get_config_color(FOREGROUND_NIGHT)
        
        self.background_color = self.background_day
        self.foreground_color = self.foreground_day;

    def read_configuration(self, config):
        
        self.set_volume(self.get_config_int(VOLUME))
        
        self.brightness_high = self.get_config_int(BRIGHTNESS_HIGH)
        self.threshold1 = self.get_config_int(THRESHOLD1)
        self.threshold2 = self.get_config_int(THRESHOLD2)
        self.brightness_low = self.get_config_int(BRIGHTNESS_LOW)
        
        self.adjustNight()
        self.in_init = False
        
#############################################################################################
    def build(self):

        tw1 = 60
        tw = 800 - 2 * tw1
        th1 = 60
        th = 480 - 2 * th1
        
        aw1 = 120
        aw = tw - 2 * aw1
        
        layout1 = GridLayout(rows=3,cols=3,
                             cols_minimum= {0:tw1, 1:tw, 2:tw1},
                             col_force_default= True,
                             rows_minimum= {0:th1, 1:th, 2:th1},
                             row_force_default= True)

        if (os.name == "nt" ):       
            self.button_switch = self._add_widget(layout1, Button(text="F1", on_press=self.switch_F1, size_hint=(.8, .8)), "")
        else:
            self.widget1_1 = self._add_widget(layout1, Label(text="1,1"), "")
            self._set_visibility_control(self.widget1_1, False)

        layout2 = GridLayout(cols=3,
                             cols_minimum= {0:aw1, 1:aw, 2:aw1},
                             col_force_default= True)
        
        self.button_alarmtime = self._add_widget(layout2, Button(text="22:30", size_hint=(.8, .8)), "", inverse=True)
        self.button_alarmtime.font_size='24dp'
        self.button_alarminfo = self._add_widget(layout2, Button(text="Radio NDR2", size_hint=(.8, .8)), "", inverse=True)
        self.button_alarminfo.font_size='32dp'
        self.label_volume = self._add_widget(layout2, Label(text="100"), "")
        self.label_volume.font_size='24dp'
        layout1.add_widget(layout2)
        
        self.button_on = self._add_widget(layout1, Button(text="an", on_press=self.switch_on, size_hint=(.8, .8)), "")
        
        self.brightslider = self._add_widget(layout1, Slider(min=0, max = 100, value = 25, size_hint=(.05, .8), orientation='vertical', step=1), "")
        self.brightslider.bind(value=self._brightness_changed)
        
        self.time = self._add_widget(layout1, Label(text=datetime.now().isoformat()[11:16]), "")
        if self.digits == 6:
            self.time.font_size='128dp'
        else:
            self.time.font_size='256dp'

        self.volslider = self._add_widget(layout1, Slider(min=0, max = 100, value = 25, size_hint=(.05, .8), orientation='vertical', step=1), "")
        self.volslider.bind(value=self._volume_changed)
        
#        self._set_visibility_control(self.widget3_1, False)
        
#        self.widget3_1 = self._add_widget(layout1, Label(text="3,1"), "")
        self.button_clean = self._add_widget(layout1, Button(text="clean", on_press=self.switch_clean, size_hint=(.8, .8)), "")
#        self._set_visibility_control(self.widget3_1, False)
        layout3 = GridLayout(cols=3,
                             cols_minimum= {0:aw1*2, 1:aw-2*aw1, 2:aw1*2},
                             col_force_default= True)
        self.widget3_2_1 = self._add_widget(layout3, Label(text="3,2,1"), "")
        self._set_visibility_control(self.widget3_2_1, False)
        self.button_stop = self._add_widget(layout3, Button(text="Stop", on_press=self.switch_stop, size_hint=(.2, .8)), "")
        self.widget3_2_3 = self._add_widget(layout3, Label(text="3,2,3"), "")
        self._set_visibility_control(self.widget3_2_3, False)
        layout1.add_widget(layout3)
        
        self.button_off = self._add_widget(layout1, Button(text="aus", on_press=self.switch_off, size_hint=(.8, .8)), "")

        self.set_visible(self.visible)

        self.root = layout1
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
        self._set_visibility_control(self.button_clean, visible)
#        self._set_visibility_control(self.button_alarminfo, visible)
        self._visible = visible

#############################################################################################
    def _handle_time(self, event):
        self.set_time(event.data)
        self.adjustNight()
#        if event.data.second == 0:
#            logger.logvalue(event.eventname, self.ambient_light)
        
    def set_time(self, time):
        self.time.text = time.isoformat()[11:self.last_time_pos]
                
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

    def switch_F1(self, instance):
#        self.raise_event(CLICK, None)
        if self.nighttime == 1:
            e = Event("Day", self.ambient_day)
        else:
            e = Event("Night", self.ambient_night)
        self._handle_ambientlight(e)
        pass

    def switch_stop(self, instance):
        if not self.clean:
            self.raise_event(STOP, None)

    def switch_clean(self, instance):
        self.set_disabled(not self.clean)
        self.raise_valuechange(CLEAN, self.clean)
#        self.set_nighttime(not self.nighttime)

    def set_disabled(self, disabled):
        self.clean = disabled
        self.button_alarmtime.disabled = disabled
        self.button_alarminfo.disabled = disabled
        self.button_on.disabled = disabled
        self.button_off.disabled = disabled
        self.volslider.disabled = disabled
        self.brightslider.disabled = disabled
        self.button_stop.disabled = disabled
        self.button_clean.disabled = disabled
 
    def _handle_enable(self, event):
        self.set_disabled(False)
    
#############################################################################################
#    def set_volume_changed(self, method, obj=None):
#        self.callback_off = classes.CallbackInfo(method)
        
    def set_volume(self, value):
#        logger.logvalue(VOLUME, value)
        valueint = int(value)
        if self.last_volume <> value and not self.clean:
            self.last_volume = value
            self.volslider.value = self.adaptor_volume.calc_display(value)
            self.label_volume.text = str(valueint)
            self.raise_valuechange(VOLUME, valueint)
            self.set_config(VOLUME, valueint)
            
    def get_volume(self):
        return self.last_volume

    def _volume_changed(self, instance, value):
        self.set_volume(self.adaptor_volume.calc_value(value))

#############################################################################################
#    def set_brightness_changed(self, method, obj=None):
#        self.callback_brightness = classes.CallbackInfo(method)
        
    def set_brightness(self, value):
#        logger.logvalue(BRIGHTNESS , value)
        valueint = int(value)
        if self.last_brightness <> value:
            lb = self.last_brightness
            self.last_brightness = value
            self.brightslider.value = self.adaptor_brightness.calc_display(value)
            self.brightness[self.nighttime] = valueint
            self.raise_valuechange(BRIGHTNESS, valueint)
            if self.nighttime == 1:
                self.set_config(BRIGHTNESS_LOW, valueint)
                self.brightness_low = valueint
                if self.user_change and self.check_threshold() == 2:
                    self.adjust_brightness()
#                    v = (((self.brightness_high - value) / (self.brightness_high - lb * 1.0)) * (self.brightness_high - self.brightness_low * 1.0))
#                    v = self.brightness_high - v
#                    v = self.brightness_low - v
#                    if (v < 10):
#                        v = 10
#                    v = int(v)
            else:
                self.set_config(BRIGHTNESS_HIGH, valueint)
                self.brightness_high = valueint
        
    def get_brightness(self):
        return self.actual_brightness

    def _brightness_changed(self, instance, value):
        self.set_brightness(self.adaptor_brightness.calc_value(value))
        
    def _handle_ambientlight(self, event):
        self.user_change = False
        self.ambient_light = event.data
        c = self.norm_color(event.data)
        self.foreground_night = c
        self.background_day = c 
        self.adjustNight()
        self.adjustColors()
        self.adjust_brightness()
        self.user_change = True
        
    def adjust_brightness(self):
        setslider = True
        if self.nighttime == 1:
            if isinstance(self.ambient_light, dict):
                al = self.ambient_light['c']
                if al < self.threshold1 and al > self.threshold2:
                    b = (1.0 * al) - self.threshold2
                    b = ((b / (self.threshold1 - self.threshold2)) * (self.brightness_high - self.brightness_low)) + self.brightness_low
                    al = (((al - self.threshold2) / (self.threshold1 - self.threshold2)) * (self.brightness_high - self.brightness_low)) + self.brightness_low
                    logger.logvalue("Brightness2", b)
                    setslider = False
                else:
                    b = self.brightness_low
            else:
                b = self.brightness_low
        else:
            b = self.brightness_high
        self.actual_brightness = b
        if self.last_brightness <> b:
            if setslider:
                self.set_brightness(b)
            else:
                self.last_brightness = self.actual_brightness
                self.raise_valuechange(BRIGHTNESS, self.actual_brightness)
            
        
    def check_threshold(self):
        t = 1
        if isinstance(self.ambient_light, dict):
            al = self.ambient_light['c']
            if al < self.threshold1:
                if al > self.threshold2:
                    t = 2
                else:
                    t = 3
        return t
        
    def norm_color(self, rgb):
        c = [rgb['r'], rgb['g'], rgb['b'], 1]
        m = c[0]
        if c[1] > m:
            m = c[1]
        if c[2] > m:
            m = c[2]
        if m > 0:
            c[0] = c[0] / (1.0 * m)  
            c[1] = c[1] / (1.0 * m)  
            c[2] = c[2] / (1.0 * m)  
            cc = Color(c[0], c[1], c[2])
        else:
            cc = self.background_day
        return cc
          
#############################################################################################
    def set_nighttime(self, value):
        if self.nighttime <> value or self.in_init:
            self.nighttime = value
            self.raise_valuechange(NIGHT_TIME, value)
            if (self.nighttime == 1):
                self.set_night_display()
            else:
                self.set_day_display()
            self.adjust_brightness()

    def get_nighttime(self):
        return self.nighttime

    def set_day_display(self):
        self.background_color = self.background_day
        self.foreground_color = self.foreground_day
        self.set_colors(self.root, self.background_color, self.foreground_color)
        pass
    
    def set_night_display(self):
        self.background_color = self.background_night
        self.foreground_color = self.foreground_night
        self.set_colors(self.root, self.background_color, self.foreground_color)
    
    def adjustColors(self):
        if self.nighttime == 1:
            self.set_night_display()
        else:
            self.set_day_display()
    
    def adjustNight(self):
        night = 0
        if isinstance(self.ambient_light, dict):
            al = self.ambient_light['c']
            if al < self.threshold1:
                night = 1
        self.set_nighttime(night)

    def set_colors(self, widget, color1, color2):
        if isinstance(widget, Layout):
            for w in widget.children:
                self.set_colors(w, color1, color2)
        elif isinstance(widget, Button):
            self._set_background_button(widget, color1, color2)
            self._set_foreground_button(widget, color1, color2)
        else:
            self._set_background(widget, color1)
            self._set_foreground(widget, color2)
        
    
#############################################################################################
#
#  internal methods
#
#############################################################################################

    def _add_widget(self, layout, widget, widget_id, inverse=False):
#        widget.color = self.foreground_color
        self._add_background(widget, self.background_color)
        widget.background_normal = ''
        widget.inverse = inverse
        if widget_id != "":
            widget.id = widget_id
        layout.add_widget(widget)
        return widget
    
    def _update_rect(self, widget, value):
        widget.rect1.pos = widget.pos
        widget.rect1.size = widget.size
        if widget.__dict__["rect2"] is not None:
            widget.rect2.pos = widget.pos
            widget.rect2.size = widget.size
    
    def _add_background(self, widget, background):
        widget.color1 = Color(0,0,0,1)
        widget.rect1 = Rectangle(pos=widget.pos, size=widget.size)
        widget.canvas.before.add(widget.color1)
        widget.canvas.before.add(widget.rect1)
        widget.bind(pos=self._update_rect, size=self._update_rect)
        widget.color0 = Color(0,0,0,1)
#        widget.canvas.before.add(widget.color0)
        
        widget.color2 = Color(0,0,0,0)
        widget.rect2 = Rectangle(pos=widget.pos, size=widget.size)
        widget.canvas.after.add(widget.color2)
        widget.canvas.after.add(widget.rect2)
        
    def _set_visibility_control(self, widget, visible):
        if widget.__dict__["color2"] is not None:
            if visible:
                widget.color2.a = 0
            else:
                widget.color2.a = 1
                
    def _set_foreground(self, widget, color):
        widget.color = color.rgba
        if widget.__dict__["color0"] is not None:
            widget.color0.r = color.r
            widget.color0.g = color.g
            widget.color0.b = color.b
                
    def _set_foreground_button(self, widget, color1, color2):
        c1 = color1
        c2 = color2
        if widget.inverse:
            c1 = color2
            c2 = color1
        widget.color = c1.rgba
        if widget.__dict__["color0"] is not None:
            widget.color0.r = c1.r
            widget.color0.g = c1.g
            widget.color0.b = c1.b
                
    def _set_foreground2(self, widget, color):
        widget.color = color
        if widget.__dict__["color0"] is not None:
            widget.color0.r = color[0]
            widget.color0.g = color[1]
            widget.color0.b = color[2]
                
    def _set_background2(self, widget, color):
        if widget.__dict__["color1"] is not None:
            widget.color1.r = color[0]
            widget.color1.g = color[1]
            widget.color1.b = color[2]
        if widget.__dict__["color2"] is not None:
            widget.color2.r = color[0]
            widget.color2.g = color[1]
            widget.color2.b = color[2]
                
    def _set_background(self, widget, color):
        if widget.__dict__["color1"] is not None:
            widget.color1.r = color.r
            widget.color1.g = color.g
            widget.color1.b = color.b
        if widget.__dict__["color2"] is not None:
            widget.color2.r = color.r
            widget.color2.g = color.g
            widget.color2.b = color.b
                
    def _set_background_button(self, widget, color1, color2):
        c1 = color1
        c2 = color2
        if widget.inverse:
            c1 = color2
            c2 = color1
        widget.background_color = c2.rgba
        
        if widget.__dict__["color1"] is not None:
            widget.color1.r = c1.r
            widget.color1.g = c1.g
            widget.color1.b = c1.b
        if widget.__dict__["color2"] is not None:
            widget.color2.r = color1.r
            widget.color2.g = color1.g
            widget.color2.b = color1.b
                
class ValueAdaptor:
    def __init__(self, offsets, limits):

        self.offsets = offsets
        self.limits = limits
        self.norm1 = [(1.0 / (limits[0][1] - limits[0][0])), (1.0 / (limits[1][1] - limits[1][0]))]
        self.norm_offsets = []
#        self.low = [low_val, low_dis]
#        self.high = [high_val, high_dis]
        
        self.norm_offsets = []
        hv = 0.0
        hd = 0.0
        for l in offsets:
            lv = hv
            ld = hd
            hv = l[0]
            hd = l[1]
            transform = [(hd - ld), (hv - lv)]
            offset = [l[0], l[1], transform]
#            offset = [l[0] * self.norm1[0], l[1] * self.norm1[1], transform]
            self.norm_offsets.append(offset)
        transform = [(1.0 - hd), (1.0 - hv)]
        self.norm_offsets.append([1.0, 1.0, transform])
        
    def calc_display(self, value):
        return self.calc(value, 0, 1)
    
    def calc_value(self, value):
        return self.calc(value, 1, 0)
    
    def calc(self, in_value, i1, i2):
        norm_in1 = (in_value - self.limits[i1][0]) * self.norm1[i1]
        h1 = 0.0
        h2 = 0.0
        out_value = 0;
        for l in self.norm_offsets:
            l1 = h1
            l2 = h2
            h1 = l[i1]
            h2 = l[i2]
            if l1 <= norm_in1 and h1 >= norm_in1:
                norm_in2 = (norm_in1 - l1) / (h1 - l1)
                norm_out2 = norm_in2 * l[2][i1]
                norm_out1 = norm_out2 + l2
                out_value = (norm_out1 / self.norm1[i2]) + self.limits[i2][0]
                break
        return round(out_value, 5)   
    
    
    
    
    
    
    
    
    
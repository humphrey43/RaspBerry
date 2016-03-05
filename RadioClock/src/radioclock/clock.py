'''
Created on 22.12.2015

@author: hardy
'''
from datetime import datetime
import kivy
import sys
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics import Color
from kivy.graphics import Rectangle

import classes
import player
import clockwork
import clockface
from kivy.uix.slider import Slider


kivy.require('1.0.7')

clockFace = None 
clockWork = None

def switch_on(instance):
    clockFace.set_visible(True)
    
def switch_off(instance):
    clockFace.set_visible(False)


class RadioClock(App):
    
    def __init__(self):
        super(RadioClock, self).__init__()
        
        musicSource = "C:/Users/hardy/Music/iTunes/iTunes Media/Music/"
    #    musicSource = "/home/pi/Music/"
        self.ndr2 = player.Source("NDR2","http://ndr-ndr2-nds-mp3.akacast.akamaistream.net/7/400/252763/v1/gnl.akacast.akamaistream.net/ndr_ndr2_nds_mp3.mp3")
        self.player = None
        self.jimi = player.Source("Jimi Hendrix",musicSource + "Jimi Hendrix Experience/The Ultimate Experience/03 Hey Joe.mp3")
    
        self.alarmedToday = False
        self.alarmTime = datetime(2016, 2, 8, 4, 58)
        
        self.alarmtypes = {}
        self.alarms = {}
        self.sources = {}
        
        clock.clockWork = clockwork.ClockWork()
        clockFace = clockface.ClockFace()
        
        i = 42

    
    def animate(self, dt):
        clockFace = datetime.now()
#        if self.checkAlarmTime():
#            self.ringAlarm()
#        self.label.refresh()


    def ringAlarm(self): 
        if self.player == None:
            self.player = player.Player()
        self.player.play(self.ndr2)

    def setTime(self,instance): 
        self.i += 1
        s = datetime.now().isoformat()[11:16]
        self.label.text = s
        self.label.padding = '10dp'
        self.label.size = self.label.texture_size

    def play(self,instance): 
        if self.player == None:
            self.player = player.Player()
            self.player.play(self.ndr2)
        elif self.player.name == "NDR2":
            self.player.play(self.jimi)
##       elif self.player.name == "Jimi Hendrix":
##            self.player.off()
##            self.player.name = ""
        else:
            sys.exit(0)
##            self.player.play(self.ndr2)
        
    def build2(self):
        w = self.root_window
        n1 = self.config.get("Test","Test1")
        Clock.schedule_interval(self.animate,5)
        
    def build(self):
        root = clockFace.build()
        clockFace.set_switch_on(switch_on)
        clockFace.set_switch_off(switch_off)
        return root

    def build_config(self, config):
        config.add_section("Test")
#        config.set("Test", "Test1", "Hardy")
        
    def volumeChanged(self, obj, vol):
        print "Volume", vol
        self.player.sound.volume = vol/100
        
    def checkAlarmTime(self):
        self.checkNewDay()
        if not self.alarmedToday and self.alarmTime <= datetime.now():
            self.alarmedToday = True
            return True
        return False
            
    def checkNewDay(self):
        s = datetime.now().isoformat()[11:16]
        if s == "00:00":
            self.alarmedToday = False
            
if __name__ == '__main__':
        RadioClock().run()


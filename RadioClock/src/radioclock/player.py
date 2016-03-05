'''
Created on 22.12.2015

@author: hardy
'''

import classes
import kivy
import sys

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from swbus import SWBusComponent

PLAYER = "Player"
SOURCE = "Source"
INFO = "Info"
PLAY = "Play"
START = "Start"
STOP = "Stop"
OFF = "Off"
REWIND = "Rewind"
VOLUME = "Volume"
FINISH = "Finish"
PLAYING = "Playing"

kivy.require('1.0.7')

class Source:
    
    TYPE_SOURCE_SOUND = "Sound"
    TYPE_SOURCE_RADIO = "Radio"
    
    def __init__(self, sourcetype, name, title, address):
        self.sourcetype = sourcetype
        self.name = name
        self.title = title
        self.address = address
        
        
class Player(SWBusComponent):
    
    def __init__(self):
        super(Player, self).__init__(PLAYER)

        self.playing = False
        self.sound = None
        self.volume = 100
        self.source = None
        
    def register(self):
        self.opt_for_event(PLAY, self._play)
        self.opt_for_event(STOP, self._stop)
        self.opt_for_event(START, self._start)
        self.opt_for_event(REWIND, self._rewind)
        self.opt_for_event(OFF, self._off)
        
        self.announce_event(FINISH)
        
        self.define_value(VOLUME)
        self.define_value(INFO)
        self.define_value(PLAYING, setter=False, valuechange=True)
        
    def bus_stop(self):
        if self.playing:
            self.off()
        self.run = False
    
    def read_configuration(self, config):
        self.config = config
        self.volume = self.get_config_value(VOLUME)
        self.in_init = False
        
#############################################################################################
    def play(self, source):
        self._assert_stop()
        self.source = source
        self.sound = SoundLoader.load(self.source.address)
        self.sound.play()
        self.set_playing(True)
    
    def stop(self):
        self._assert_stop()
    
    def start(self):
        if self.sound != None:
            self.sound.play()
            self.set_playing(True)
    
    def rewind(self):
        if self.sound != None and self.source.sourcetype == Source.TYPE_SOURCE_SOUND:
            self.sound.stop()
            self.sound.seek(0)
            self.sound.play()
            self.set_playing(True)

    def off(self):
        if self._assert_stop():
            self.sound.unload()
            self.sound = None

    def _assert_stop(self):
        sound_stopped = False
        if self.sound != None:
            if self.sound.state == 'play':
                self.sound.stop()
                self.set_playing(False)
            sound_stopped = True
        return sound_stopped
    
    def set_volume(self, volume):
        self.volume = volume
        if self.volume < 0:
            self.volume = 0
        if self.volume > 100:
            self.volume = 100
        if self.sound is not None:
            self.sound.volume = volume / 100
        
    def get_info(self):
        info = ""
        if self.source is not None:
            info = self.source.sourcetype + " " + self.source.title
        return info
        
    def set_playing(self, playing):
        if self.playing is not playing:
            self.playing = playing
            self.raise_valuechange(PLAYING, self.playing)
        return self.playing
        
    def get_playing(self):
        return self.playing
        
#############################################################################################
    def _play(self, event):
        self.play(event.data)
    
    def _stop(self, event):
        self.stop
    
    def _start(self, event):
        self.start
    
    def _rewind(self, event):
        self.rewind

    def _off(self, event):
        self.off
    


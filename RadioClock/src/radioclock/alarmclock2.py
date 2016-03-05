'''
Created on 22.12.2015

@author: hardy
'''
from datetime import datetime, timedelta

import sys

import classes
import player

class AlarmType:
    
    TYPE_SOURCE_RADIO = "Radio"
    TYPE_SOURCE_SOUND = "Sound"
    
    def __init__(self):
        self.__class_name__ = "AlarmType"
        self.name = ""
        self.source1 = None
        self.source_type1 = None
        self.source_name1 = None
        self.source2 = None
        self.source_type2 = None
        self.source_name2 = None
        self.source2 = None
        self.off_after = 60

class Alarm:
    
    DAYS_ALL = "MO-SO"
    DAYS_WEEK = "MO-FR"
    DAYS_WEEKEND = "SA-SO"
    DAYS_NONE = "NONE"
    DAY_MONDAY = "MO"
    DAY_TUESDAY = "DI"
    DAY_WEDNESYDAY = "MI"
    DAY_THURSDAY = "DO"
    DAY_FRIDAY = "FR"
    DAY_SATURDAY = "SA"
    DAY_SUNDAY = "SO"
    DAY_NEXT = ""
    
    DAYS = (DAY_MONDAY,
            DAY_TUESDAY,
            DAY_WEDNESYDAY,
            DAY_THURSDAY,
            DAY_FRIDAY,
            DAY_SATURDAY,
            DAY_SUNDAY)

    SET_DAYS_WEEK = set([DAY_MONDAY,
            DAY_TUESDAY,
            DAY_WEDNESYDAY,
            DAY_THURSDAY,
            DAY_FRIDAY])

    SET_DAYS_WEEKEND = set([DAY_SATURDAY,
            DAY_SUNDAY])

    SET_DAYS_ALL = set([DAY_MONDAY,
            DAY_TUESDAY,
            DAY_WEDNESYDAY,
            DAY_THURSDAY,
            DAY_FRIDAY,
            DAY_SATURDAY,
            DAY_SUNDAY])

    
    def __init__(self, day=DAYS_ALL, hour = 0, minute = 0, alarmtype = "STANDARD"):
        self.__class_name__ = "Alarm"
        self.day = day
        self.hour = hour
        self.minute = minute
        self.alarmtype = alarmtype
        self.alarmed = False;
        self.set_level()
                
    def set_level(self):
        if self.day == Alarm.DAYS_ALL:
            self.level = 3
        elif self.day == Alarm.DAYS_WEEK or self.day == Alarm.DAYS_WEEKEND:
            self.level = 2
        elif self.day == Alarm.DAY_NEXT:
            self.level = 0
        else: 
            self.level = 1

    def is_passed(self):
        now = datetime.now()
        if now.hour > self.hour:
            passed = True
        elif now.hour == self.hour and now.minute > self.minute:
            passed = True
        else:
            passed = False
        return passed
    
class ClockWork:

    def __init__(self):
        self.__class_name__ = "ClockWork"
        self.day = Alarm.DAYS_ALL
        self.hour = 0
        self.minute = 0
        self.alarmtype = "STANDARD"
        
        self.alarmed_today = False
        self.next_alarm = None
        self.next_alarmtime = datetime(2016, 2, 8, 4, 58)
        
        self.alarmtypes = {}
        self.alarms = {}
        self.set_alarm(Alarm.DAYS_WEEK, 4, 58, "STANDARD")
        self.set_alarm(Alarm.DAYS_WEEKEND, 8, 30, "STANDARD")
        self.set_next_alarm()
        print self.next_alarm
        print self.next_alarmtime

    def set_alarm(self, day, hour, minute, alarmtype):
        alarm = Alarm(day, hour, minute, alarmtype)
        self.alarms[day] = alarm
        self.set_next_alarm()
        
    def set_next_alarm(self):
        now = datetime.now()
        tomorrow = now + timedelta(1)
        wd_today = Alarm.DAYS[now.weekday()]
        wd_tomorrow = Alarm.DAYS[tomorrow.weekday()]
        alarm_today = self.get_alarm_for_day(wd_today)
        alarm_tomorrow = self.get_alarm_for_day(wd_tomorrow)
        self.next_alarm = None
        self.next_alarmtime = None
        if alarm_today is not None and not alarm_today.is_passed():
            self.next_alarm = alarm_today
            self.next_alarmtime = datetime(now.year, now.month, now.day, self.next_alarm.hour, self.next_alarm.minute)
        elif alarm_tomorrow is not None:
            self.next_alarm = alarm_tomorrow
            self.next_alarmtime = datetime(tomorrow.year, tomorrow.month, tomorrow.day, self.next_alarm.hour, self.next_alarm.minute)

    def get_alarm_for_day(self, weekday):
        erg = None
        last_level = 4
        for alarm in self.alarms.values():
            if alarm.level < last_level:
                if (alarm.level == 0 or
                    alarm.day == weekday or
                    alarm.day == Alarm.DAYS_ALL or
                    (alarm.day == Alarm.DAYS_WEEK and weekday in Alarm.SET_DAYS_WEEK) or 
                    (alarm.day == Alarm.DAYS_WEEKEND and weekday in Alarm.SET_DAYS_WEEKEND)):
                    erg = alarm
                    last_level = alarm.level
        return erg
                    
        
#    musicSource = "C:\Users\hardy\Music\iTunes\iTunes Media\Music\"
    musicSource = "/home/pi/Music/"
    ndr2 = player.Source("NDR2","http://ndr-ndr2-nds-mp3.akacast.akamaistream.net/7/400/252763/v1/gnl.akacast.akamaistream.net/ndr_ndr2_nds_mp3.mp3")
    player2 = None
    jimi = player.Source("Jimi Hendrix",musicSource + "Jimi Hendrix Experience/The Ultimate Experience/03 Hey Joe.mp3")

    
#    Window.fullscreen = True
    def animate(self, dt):
        s = datetime.now().isoformat()[11:19]
        self.label.text = s
        if self.checkAlarmTime():
            self.ringAlarm()
#        self.label.refresh()


    def ringAlarm(self): 
        if self.player == None:
            self.player = player()
        self.player.play(self.ndr2)

    def setTime(self,instance): 
        self.i += 1
        s = datetime.now().isoformat()[11:19]
        self.label.text = s
        self.label.padding = '10dp'
        self.label.size = self.label.texture_size

    def play(self,instance): 
        if self.player == None:
            self.player = player()
            self.player.play(self.ndr2)
        elif self.player.name == "NDR2":
            self.player.play(self.jimi)
##       elif self.player.name == "Jimi Hendrix":
##            self.player.off()
##            self.player.name = ""
        else:
            sys.exit(0)
##            self.player.play(self.ndr2)
        
    def checkAlarmTime(self):
        self.checkNewDay()
        if not self.alarmed_today and self.alarmTime <= datetime.now():
            self.alarmed_today = True
            return True
        return False
            
    def checkNewDay(self):
        s = datetime.now().isoformat()[11:16]
        if s == "00:00":
            self.alarmed_today = False

classes.registerClass("Alarm", Alarm)
classes.registerClass("AlarmType", AlarmType)


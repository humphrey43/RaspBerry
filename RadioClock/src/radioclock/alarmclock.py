'''
Created on 22.12.2015

@author: hardy
'''
from datetime import datetime, timedelta

from swbus import SWBusComponent

import classes

ALARM_CLOCK = "AlarmClock"
ALARM = "Alarm"
ALARM_TIME = "AlarmTime"
ALARM_INFO = "AlarmInfo"
ALARM_LIST = "AlarmList"
LAST_ALARM = "LastAlarm"
TIME = "Time"
DATETIME_MINUTE_FORMAT = "%Y.%m.%d %H:%M"
TIME_MINUTE_FORMAT = "%H:%M"

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
    
class AlarmClock(SWBusComponent):

    def __init__(self):
        super(AlarmClock, self).__init__(ALARM_CLOCK)

        self.last_alarm = datetime.now()
        self.next_alarm = None
        
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

#############################################################################################
#
#   Methods for SWBusComponent
#
#############################################################################################
    def register(self):
        self.opt_for_event(TIME, self._handle_time)
        
        self.announce_event(ALARM)
        
        self.define_value(ALARM_TIME, valuechange=True)
        self.define_value(ALARM_INFO, valuechange=True)
        self.define_value(ALARM_LIST, valuechange=True)
        
    def read_configuration(self, config):
        self.config = config

        la = self.get_config_value(LAST_ALARM)
        if la is not None and la <> "":
            self.last_alarm = datetime.strptime(la, DATETIME_MINUTE_FORMAT)
        self.in_init = False
        
#############################################################################################
#
#   Methods for Events and Values
#
#############################################################################################
    def _handle_time(self, event):
        self.check_alarm_time(event.data)

#############################################################################################
#
#   Methods for Events and Values
#
#############################################################################################
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


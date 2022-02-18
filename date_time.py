import datetime
from utils import time_obj, date_obj, combine_date_time

TODAY = datetime.datetime.now().date().strftime('%Y-%m-%d')

class Time:
    def __init__(self, time):
        self.obj = time_obj(time)
        if isinstance(self.obj, datetime.time):
            self.hours = self.obj.hour
            self.minutes = self.obj.minute
            self.readable = self.obj.strftime('%#H:%M')              # this works on windows, for linux replace '#' for '-'
            self.readable_ampm = self.obj.strftime('%#I:%M %p')      # this works on windows, for linux replace '#' for '-'

class Date:
    def __init__(self, date=TODAY):
        self.obj = date_obj(date)
        if isinstance(self.obj, datetime.date):
            self.day = self.obj.day
            self.month = self.obj.month
            self.year = self.obj.year
            self.readable = f"{self.month:02}/{self.day:02}/{self.year}"

class DateObj:
    def __init__(self, time, date=TODAY):
        self.time_obj = Time(time).obj
        self.date_obj = Date(date).obj
        self.obj = combine_date_time(Date(date).obj, Time(time).obj)

    def add_minutes(self, minutes=60):
        self.obj += datetime.timedelta(minutes=minutes)
        hours = self.time_obj.hour + (minutes // 60)
        minutes = self.time_obj.minute + (minutes % 60)
        self.time_obj = self.time_obj.replace(hour=hours, minute=minutes)

    @property
    def readable(self):
        return self.obj.strftime('%m/%d/%Y %#H:%M')      # this works on windows, for linux replace '#' for '-'

    @property
    def time(self):
        return self.obj.strftime('%#H:%M')      # this works on windows, for linux replace '#' for '-'

    @property
    def date(self):
        return self.obj.strftime('%m/%d/%Y')      # this works on windows, for linux replace '#' for '-'


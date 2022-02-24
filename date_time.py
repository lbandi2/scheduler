import datetime
from utils import time_obj, date_obj, combine_date_time
from utils import weekend, first_weekday_x_months, format_dt, round_time

class Time:
    def __init__(self, time='undefined'):
            # print("[NOTE] Using the next hour")
        time = self._time_code_words(time)
        self.obj = time_obj(time)
        if isinstance(self.obj, datetime.time):
            self.hours = self.obj.hour
            self.minutes = self.obj.minute
            self.readable = self.obj.strftime(format_dt('%-H:%M'))
            self.readable_ampm = self.obj.strftime(format_dt('%-I:%M %p'))

    def _time_code_words(self, item):
        now_time = datetime.datetime.now().time()
        if item == 'undefined' or item == '' or item == '0m':
            return now_time
        else:
            if type(item) == datetime.time:
                return item
            if (type(item) == str or type(item) == int) and str(item).isdigit():
                return item
            elif not str(item).isdigit() and 2 <= len(item) <= 6:
                return round_time(now_time, item)
            else:
                print(f"[ERROR] Code word of type {type(item).__name__} is not allowed for Time object") #FIXME: is this necessary?

    def is_valid(self):  #FIXME: Decorator?
        if self.obj:
            return True
        return False

class Date:
    def __init__(self, date='undefined', weekends=False):
            # print("[NOTE] Using today's date")
        date = self._date_code_words(date, weekends)
        self.obj = date_obj(date)
        if isinstance(self.obj, datetime.date):
            self.day = self.obj.day
            self.month = self.obj.month
            self.year = self.obj.year
            self.readable = f"{self.month:02}/{self.day:02}/{self.year}"

    def _date_code_words(self, item, weekends):
        today = datetime.datetime.now().date()
        if item == 'undefined' or item == '' or item == '0d':
            return today
        else:
            if type(item) == datetime.date:
                return item
            if type(item) == str or type(item) == int:
                if str(item).isdigit():
                    return item
                elif 2 <= len(item) <= 3 and not item.isdigit():
                    amount = int(item[:-1])
                    if 'd' in item:
                        return today + datetime.timedelta(days=amount)
                    elif 'w' in item:
                        return today + datetime.timedelta(days=(7 * amount - today.weekday()))
                    elif 'm' in item:
                        return first_weekday_x_months(weekends, date=today, months=1 * amount)
            else:
                print(f"[ERROR] Code word of type {type(item).__name__} is not allowed for Date object") #FIXME: is this necessary?

    def is_valid(self):
        if self.obj:
            return True
        return False

    @property
    def is_weekend(self):
        return weekend(self.obj)

class DateObj:
    def __init__(self, time='undefined', date='undefined'):
        self.obj = None
        if Time(time).is_valid() and Date(date).is_valid():
            self.obj = combine_date_time(Date(date).obj, Time(time).obj)

    def is_valid(self):
        if self.obj is not None:
            return True
        return False

    def add_minutes(self, minutes=60):
        self.obj += datetime.timedelta(minutes=minutes)

    @property
    def time_obj(self):
        return self.obj.time()

    @property
    def date_obj(self):
        return self.obj.date()

    @property
    def readable(self):
        return self.obj.strftime(format_dt('%m/%d/%Y %#H:%M'))

    @property
    def time(self):
        return self.obj.strftime(format_dt('%#H:%M'))

    @property
    def date(self):
        return self.obj.strftime(format_dt('%m/%d/%Y'))

    @property
    def is_weekend(self):
        return weekend(self.obj)

import datetime
from date_time import DateObj

class Appointment:
    TODAY = datetime.datetime.now().date().strftime('%Y-%m-%d')

    def __init__(self, start_time, start_date=TODAY, **kwargs):
        self.start = DateObj(start_time, start_date)
        self.end = DateObj(start_time, start_date)
        if 'length' in kwargs:
            self.end.add_minutes(kwargs['length'])
        else:
            self.end.add_minutes(60)
        if 'end_date' in kwargs and 'end_time' not in kwargs:
            self.end = DateObj(start_time, kwargs['end_date'])
        if 'end_time' in kwargs and 'end_date' not in kwargs:
            self.end = DateObj(kwargs['end_time'])
        if 'end_time' in kwargs and 'end_date' in kwargs:
            self.end = DateObj(kwargs['end_time'], kwargs['end_date'])
        self.title = "New appointment"
        if 'title' in kwargs:
            self.title = kwargs['title']
        self.importance = "default"
        if 'importance' in kwargs:
            self.importance = kwargs['importance']

    def __repr__(self):
        return f"{self.start.date} [{self.start.time}-{self.end.time}]: '{self.title}' ({self.length})"

    @property
    def length(self):
        return (self.end.obj - self.start.obj).seconds // 60

    @property
    def weekday(self):
        return self.start.obj.weekday()

from date_time import DateObj

class Appointment:
    def __init__(self, start=None, **kwargs):         #FIXME: Tidy up all this constructor
        start_time = ''
        start_date = ''
        self.start = None
        self.end = None
        self.title = "New appointment"
        self.importance = "default"
        self.silent = False
        if "silent" in kwargs:
            self.silent = kwargs['silent']
        if "start_date" in kwargs:
            if kwargs["start_date"] != '0d':
                start_date = kwargs['start_date']
                start_time = start                    # set time to start of schedule day if date is different from today
        if "start_time" in kwargs:
            start_time = kwargs['start_time']
        end_time = start_time
        end_date = start_date
        if "end_time" in kwargs:
            end_time = kwargs['end_time']
        if "end_date" in kwargs:
            end_date = kwargs['end_date']
        if "title" in kwargs:
            self.title = kwargs['title']
        if "importance" in kwargs:
            self.importance = kwargs['importance']
        self.start = DateObj(start_time, start_date)
        if self.start.is_valid():
            self.end = DateObj(end_time, end_date)
        if self.is_valid():
            if "end_time" not in kwargs:
                if "length" in kwargs:
                    self.end.add_minutes(int(kwargs['length']))
                else:
                    self.end.add_minutes(30)

    def is_valid(self):   #TODO: Decorator?
        try:
            if self.start.obj is not None and self.end.obj is not None:
                return True
            return False
        except AttributeError:
            return False

    def __repr__(self):
        return f"{self.start.date} [{self.start.time}-{self.end.time}]: '{self.title}' ({self.length}) {'[▲]' if self.importance == 'high' else '[▼]'}"

    @property
    def length(self):
        return (self.end.obj - self.start.obj).seconds // 60

    @property
    def weekday(self):
        return self.start.obj.weekday()

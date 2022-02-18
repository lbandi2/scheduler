from calendar import week
import datetime
from os import stat
from date_time import DateObj, Date, Time
# from utils import validate_time, time_print, time_obj

class Schedule:
    def __init__(self, owner, start='9:00', end='17:00', duplicates=False, weekends=False):   ### usar **kwargs
        self.appointments = []
        self.owner = owner
        self.start = Time(start)
        self.end = Time(end)
        self.valid_args = ['start_time', 'start_date', 'end_time', 'end_date', 'title', 'importance', 'length']
        self.duplicates = duplicates
        self.weekends = weekends
        # festives with locale?

    def toggle_duplicates(self):
        if self.duplicates:
            self.duplicates = False
            print("Duplicates disabled.")
        else:
            self.duplicates = True
            print("Duplicates enabled.")

    def toggle_weekends(self):
        if self.weekends:
            self.weekends = False
            print("Weekends disabled.")
        else:
            self.weekends = True
            print("Weekends enabled.")

    @property
    def total(self):
        print(f"{self.owner} has {len(self.appointments)} appointments")
        return len(self.appointments)

    def list(self, items=None):
        if items is None:
            items = self.appointments

        if items != [] and items is not None:
            for index, appt in enumerate(items, start=1):
                print(f"{index}. {appt}")
            print(f"Found {len(items)} appointments")
        else:
            print("No appointments found.")

    def _check_args(self, args):
        """
        Checks for valid keyword arguments
        """
        for key, value in args.items():
            if key not in self.valid_args:
                print(f"Invalid keyword argument, valid arguments are: {', '.join(self.valid_args)}")
                return False
        return True

    def _work_hours(self, start_time):
        """
        Checks time object against work hours
        """
        if start_time >= self.start.obj and start_time < self.end.obj:
            return True
        print(f"Current workday is from {self.start.readable} to {self.end.readable}")
        return False

    def conflict(self, item):
        print(f"There's another appointment from {item.start.time} to {item.end.time}")

    def _dupe_check(self, start, end):
        """
        Checks if there's a previous appointment within the defined time before creation
        """
        if self.appointments == []:
            return True
        for item in self.appointments:
            if start <= item.start.obj < end:    # starts before, ends after or during
                self.conflict(item)
                return False
            elif item.start.obj <= start < item.end.obj:  # starts after, ends before or during
                self.conflict(item)
                return False
        else:
            return True

    def sort(self):
        self.appointments = sorted(self.appointments, key=lambda x: x.start.obj)

    def _do_add(self, appt):
        self.appointments.append(appt)
        print(f"Appointment added.")
        self.sort()

    def add(self, start_time, **kwargs):
        start = Time(start_time)
        if isinstance(start.obj, datetime.time):
            if self._check_args:
                if self._work_hours(start.obj):
                    appt = Appointment(start_time, **kwargs)
                    if self.duplicates:
                        self._do_add(appt)
                    else:
                        if self._dupe_check(appt.start.obj, appt.end.obj):
                            self._do_add(appt)

    def search(self, **kwargs):
        items = []
        if self._check_args(kwargs):
            for kwarg_key, kwarg_value in kwargs.items():
                for item in self.appointments:
                    if kwarg_key == 'start_time':
                        if Time(kwarg_value).obj == item.start.time_obj:
                            items.append(item)
                    if kwarg_key == 'start_date':
                        if Date(kwarg_value).obj == item.start.date_obj:
                            items.append(item)
                    if kwarg_key == 'end_time':
                        if Time(kwarg_value).obj == item.end.time_obj:
                            items.append(item)
                    if kwarg_key == 'end_date':
                        if Date(kwarg_value).obj == item.end.date_obj:
                            items.append(item)
                    if kwarg_key == 'title':
                        if kwarg_value.lower() in item.title.lower():
                            items.append(item)
                    if kwarg_key == 'importance':
                        if kwarg_value == item.importance:
                            items.append(item)
                    if kwarg_key == 'length':
                        if kwarg_value == item.length:
                            items.append(item)
            return items

    def find(self, **kwargs):
        items = self.search(**kwargs)
        self.list(items)

    def count_items(self, **kwargs):
        items = self.search(**kwargs)
        return (len(items))

    def rem(self, **kwargs):
        items = self.search(**kwargs)
        if 0 < self.count_items(**kwargs) < 2:
            print("Deleting item", items[0])
            self.appointments.remove(items[0])
        else:
            print(f"Found {len(items)} items, cannot delete unless it's one item")

    def edit(self, **kwargs):
        pass

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


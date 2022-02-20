import datetime
from date_time import Date, Time
from appointment import Appointment

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
        # first dow?
        # change work hours / ignore

    def toggle_duplicates(self):
        if self.duplicates:
            self.duplicates = False
            print("[INFO] Duplicates disabled.")
        else:
            self.duplicates = True
            print("[INFO] Duplicates enabled.")

    def toggle_weekends(self):
        if self.weekends:
            self.weekends = False
            print("[INFO] Weekends disabled.")
        else:
            self.weekends = True
            print("[INFO] Weekends enabled.")

    @property
    def total(self):
        print(f"{self.owner} has {len(self.appointments)} appointments")
        return len(self.appointments)

    def list(self, items=None):
        ignore_totals = True
        if items is None:
            items = self.appointments
            ignore_totals = False

        if items != [] and items is not None:
            for index, appt in enumerate(items, start=1):
                print(f"{index}. {appt}")
            if not ignore_totals:
                print(f"Found {len(items)} appointments")
        else:
            print("No appointments found.")

    def _check_args(self, args):
        """
        Checks for valid keyword arguments
        """
        if args == {}:
            print(f"[WARN] Missing keyword argument, valid arguments are: {', '.join(self.valid_args)}")
            return False
        for key, value in args.items():
            if key.lower() not in self.valid_args:
                print(f"[WARN] Invalid keyword argument '{key}', valid arguments are: {', '.join(self.valid_args)}")
                return False
        return True

    def _check_weekend(self, start_date):
        """
        Checks date object against weekends attribute
        """
        if not self.weekends:
            if start_date.start.obj.weekday() > 4:
                print("[WARN] Weekends are not enabled")
                print("[NOTE] Try enabling weekends with 'toggle_weekends()'")
                return False
        return True

    def _work_hours(self, start_time):
        """
        Checks time object against work hours
        """
        if start_time >= self.start.obj and start_time < self.end.obj:
            return True
        print(f"[WARN] Current workday is from {self.start.readable} to {self.end.readable}")
        return False

    def conflict(self, item):
        print(f"[WARN] There's another appointment from {item.start.time} to {item.end.time}")
        print("[NOTE] Try enabling duplicates with 'toggle_duplicates()'")

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
        print(f"[ADD] -> {appt}")
        self.sort()

    def add(self, start_time, **kwargs):
        start = Time(start_time)
        if isinstance(start.obj, datetime.time):
            if self._check_args:
                if self._work_hours(start.obj):
                    appt = Appointment(start_time, **kwargs)
                    if self._check_weekend(appt):
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
        if self._check_args(kwargs):
            items = self.search(**kwargs)
            self.list(items)
            if len(items) > 0:
                while True:
                    value = input("\n1. Edit\n2. Delete\n3. Exit\n\nOption: ")
                    if value == '1':
                        pass
                    elif value == '2':
                        self.rem(items[0])
                    elif value == '3':
                        break

    def rem(self, item=None, **kwargs):
        """
        Removes an appointment by keyword search or by accepting an appointment object
        """
        if item is None:
            if self._check_args(kwargs):
                items = self.search(**kwargs)
                if 0 < len(self.search(**kwargs)) < 2:
                    print(f"[DELETE] -> {items[0]}")
                    self.appointments.remove(items[0])
                else:
                    if len(self.appointments) == 0:
                        self.list()
                    else:
                        while True:
                            print(f"[WARN] Found {len(items)} items, cannot delete unless search criteria matches one item")
                            self.list(items)
                            value = input("Delete anyway? (Y/N): ")
                            if value.lower() == 'y':
                                for x in items:
                                    print(x)
                                    self.rem(x)   ### fails when more than one item (duplicates)
                                break
                            if value.lower() == 'n':
                                break

        else:
            if self._check_args(kwargs):
                print("[DELETE] ->", item)
                self.appointments.remove(item)

    def edit(self, **kwargs):
        pass


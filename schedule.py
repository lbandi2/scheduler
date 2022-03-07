from date_time import Date, Time
from appointment import Appointment

class Schedule:
    def __init__(self, **kwargs):
        self.appointments = []
        self.start = Time(9)           #TODO: check that end time is bigger than start
        self.end = Time(17)
        self.owner = None
        self.duplicates = False
        self.weekends = False          #TODO: option to completely ignore schedule times
        if 'start' in kwargs:
            self.start = Time(kwargs['start'])
        if 'end' in kwargs:
            self.end = Time(kwargs['end'])

    def change_work_hours(self, lst):  #TODO: add option to work night shift, ie: from 19:00 to 04:00
        self.start = Time(lst[0])
        self.end = Time(lst[1])
        print(f"[NOTE] Work hours changed to {self.start.readable} - {self.end.readable}")

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
        print(f"Total: {len(self.appointments)} appointments")
        return len(self.appointments)

    def list(self, items=None):
        if items is None:
            items = self.appointments

        if items != []:
            for index, appt in enumerate(items, start=1):
                print(f"{index}. {appt}")
            print(f"Found {len(items)} appointments")
        else:
            print("No appointments found.")

    def _check_weekend(self, start_date):
        """
        Checks date object against weekends attribute
        """
        if not self.weekends:
            if start_date.is_weekend:
                print("[WARN] Weekends are not enabled")
                print("[NOTE] Try enabling weekends with 'toggle_weekends()'")
                return False
        return True

    def _is_work_hours(self, start_time):
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
            if start <= item.start.obj < end or item.start.obj <= start < item.end.obj:
                self.conflict(item)
                return False
        else:
            return True

    def sort(self):
        self.appointments = sorted(self.appointments, key=lambda x: x.start.obj)

    def _do_add(self, appt):
        self.appointments.append(appt)
        print(f"[ADD] -> {appt} [OK]")
        self.sort()

    def add(self, **kwargs):  #TODO: decorators for all the valid stuff?
        appt = Appointment(self.start.obj, **kwargs)
        if appt.is_valid():
            if self._is_work_hours(appt.start.time_obj):
                if self._check_weekend(appt.start):
                    if self.duplicates:
                        self._do_add(appt)
                    else:
                        if self._dupe_check(appt.start.obj, appt.end.obj):
                            self._do_add(appt)

    def _search(self, **kwargs):
        items = []
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
        items = self._search(**kwargs)
        self.list(items)

    def rem(self, **kwargs):
        """
        Removes an appointment by keyword search
        """
        items = self._search(**kwargs)
        if len(items) == 0:
            self.find(**kwargs)
        elif 0 < len(items) < 2 or ('force' in kwargs and kwargs['force'] == True):
            for item in items:
                print(f"[DEL] -> {item} [OK]")
                self.appointments.remove(item)
        else:
            while True:
                print(f"[WARN] Found {len(items)} items, cannot delete unless search criteria matches one item")
                self.list(items)
                value = input("Delete anyway? (Y/N): ")
                if value.lower() == 'y':
                    for x in items:
                        self.rem(force=True, **kwargs)
                    break
                if value.lower() == 'n':
                    break

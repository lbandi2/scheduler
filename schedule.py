from utils import relative_date
from date_time import Date, Time
from appointment import Appointment
from file_operations import File

class Schedule:
    def __init__(self, **kwargs):
        self.appointments = []
        self.start = Time(9)           #TODO: check that end time is bigger than start
        self.end = Time(17)
        self.owner = None
        self.ignore_duplicates = True
        self.ignore_weekends = True
        self.ignore_work_hours = False
        if 'start' in kwargs:
            self.start = Time(kwargs['start'])
        if 'end' in kwargs:
            self.end = Time(kwargs['end'])
        if 'owner' in kwargs:
            self.owner = kwargs['owner']
            self.file = File(f"{self.owner}.json")
            self._load_save_file()
        self.info()
        self.help()

    def info(self):
        print(f"[INFO] Workday hours are from {self.start.readable_ampm} to {self.end.readable_ampm} and are {'OFF' if self.ignore_work_hours else 'ON'}")
        print(f"[INFO] Duplicates are {'OFF' if self.ignore_duplicates else 'ON'}")
        print(f"[INFO] Weekends are {'OFF' if self.ignore_weekends else 'ON'}")

    def help(self):
        print(f"[HELP] Try using add() or add(start_date='2d') or add(start_time=14) or add(start_date='1d', start_time=11, length=90)")

    def _load_save_file(self):
        # file = File(f"{self.owner}.json")
        if self.file.file is not None:
            appts = self.file.read_appts()
            self.weekends = self.file.read_setting('weekends')
            self.duplicates = self.file.read_setting('duplicates')
            start = Time(self.file.read_setting('work_hours')['start'])
            end = Time(self.file.read_setting('work_hours')['end'])
            self.change_work_hours([start.obj, end.obj], silent=True)
            if appts is not None:
                for appt in appts:
                    self.add(
                        start_date = appt['start_date'], 
                        start_time = appt['start_time'], 
                        end_date = appt['end_date'], 
                        end_time = appt['end_time'],
                        title = appt['title'],
                        importance = appt['importance'],
                        silent = True
                        )

    def _save_file(self):
        pass

    def change_work_hours(self, lst, silent=False):  #TODO: add option to work night shift, ie: from 19:00 to 04:00
        if isinstance(lst, list):
            self.start = Time(lst[0])
            self.end = Time(lst[1])
            if not silent:
                print(f"[NOTE] Work hours changed to {self.start.readable} - {self.end.readable}")
        else:
            print("[WARN] Work hours argument must be a list, ie: [9, 16]")

    def toggle_duplicates(self):
        if self.ignore_duplicates:
            self.ignore_duplicates = False
            print("[INFO] Duplicates enabled.")
        else:
            self.ignore_duplicates = True
            print("[INFO] Duplicates disabled.")

    def toggle_weekends(self):
        if self.ignore_weekends:
            self.ignore_weekends = False
            print("[INFO] Weekends enabled.")
        else:
            self.ignore_weekends = True
            print("[INFO] Weekends disabled.")

    def toggle_workhours(self):
        if self.ignore_work_hours:
            self.ignore_work_hours = False
            print("[INFO] Work hours enabled.")
        else:
            self.ignore_work_hours = True
            print("[INFO] Work hours disabled.")

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
        if self.ignore_weekends:
            if start_date.is_weekend:
                print("[WARN] Weekends are not enabled")
                print("[NOTE] Try enabling weekends with 'toggle_weekends()'")
                return False
        return True

    def _is_work_hours(self, start_time):
        """
        Checks time object against work hours
        """
        if self.ignore_work_hours:
            return True
        if start_time >= self.start.obj and start_time < self.end.obj:
            return True
        print(f"[WARN] Current workday is from {self.start.readable} to {self.end.readable}")
        print(f"[NOTE] Try changing workday hours with 'change_work_hours([9, 17])'")
        return False

    def conflict(self, item):
        print(f"[WARN] There's another appointment {relative_date(item.start.obj)} from {item.start.time} to {item.end.time}")
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

    def _save_changes(self):
        if self.file is not None:
            self.file.save_all(
                owner=self.owner,
                work_hours_start = self.start.readable,
                work_hours_end = self.end.readable,
                ignore_work_hours = self.ignore_work_hours,
                ignore_weekends = self.ignore_weekends,
                ignore_duplicates = self.ignore_duplicates,
                appts_list = self.appointments
            )

    def _do_add(self, appt):
        self.appointments.append(appt)
        if not appt.silent:
            print(f"[ADD] -> {relative_date(appt.start.obj)} [{appt.start.time}-{appt.end.time}]: '{appt.title}' ({appt.length}) [OK]")
        self.sort()
        self._save_changes()

    def add(self, **kwargs):  #TODO: decorators for all the valid stuff?
        appt = Appointment(self.start.obj, **kwargs)
        if appt.is_valid():
            if self._is_work_hours(appt.start.time_obj):
                if self._check_weekend(appt.start):
                    if not self.ignore_duplicates:
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
        self._save_changes()

import json
from utils import file_exists

class File:
    def __init__(self, filename):
        self.filename = filename
        self.file = self.open()

    def open(self):
        try:
            with open(self.filename, 'r') as f:
                content = json.load(f)
        except FileNotFoundError:
            content = self.create_file()
        else:
            print(f"[NOTE] File '{self.filename}' loaded")
            return content

    def create_file(self):
        if not file_exists(self.filename):   #TODO: Continue this
            with open(self.filename.lower(), 'w') as fp:
                pass

    def read_setting(self, setting):
        if self.file is not None and self.is_key(setting):
            return self.file[setting]
        return None

    def is_key(self, key):
        try:
            if key in self.file:
                return True
            return False
        except TypeError or KeyError:
            return False
    
    def read_appts(self):
        if self.is_key('type'):
            try:
                if self.file['type'] == 'Scheduler JSON save file':
                    pass
            except KeyError or TypeError:
                print("[ERROR] Not a valid scheduler save file")
                return None
            else:
                return self.file['appointments']

    def save_all(self, **kwargs):
        appts = []
        appts_dict = dict()
        for appt in kwargs['appts_list']:
            appts_dict['start_date'] = appt.start.date
            appts_dict['start_time'] = appt.start.time
            appts_dict['end_date'] = appt.end.date
            appts_dict['end_time'] = appt.end.time
            appts_dict['title'] = appt.title
            appts_dict['importance'] = appt.importance
            appts.append(appts_dict)
            appts_dict = dict()

        json_dict = {
            "type": "Scheduler JSON save file",
            "owner": kwargs['owner'],
            "work_hours": {
            "start": kwargs['work_hours_start'],
            "end": kwargs['work_hours_end']
            },
            "ignore_work_hours": f"{kwargs['ignore_work_hours']}",
            "ignore_weekends": f"{kwargs['ignore_weekends']}",
            "ignore_duplicates": f"{kwargs['ignore_duplicates']}",
            "appointments": appts
        }

        with open(self.filename, 'w') as f:
            json.dump(json_dict, f, indent=4)

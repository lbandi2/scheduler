from datetime import datetime as dt
import datetime
import os

def print_red(skk): print("\033[91m {}\033[00m" .format(skk))
def print_green(skk): print("\033[92m {}\033[00m" .format(skk))
def print_yellow(skk): print("\033[93m {}\033[00m" .format(skk))

def colorize(msg, color):
    if color == 'red':
        return f"\033[91m{msg}\033[00m"
    elif color == 'green':
        return f"\033[92m{msg}\033[00m"
    elif color == 'yellow':
        return f"\033[93m{msg}\033[00m"
    elif color == 'cyan':
        return f"\033[96m{msg}\033[00m"
    elif color == 'purple':
        return f"\033[94m{msg}\033[00m"

def print_box(msg, type='info', color='default'):
    if 'ON' in msg:
        msg = msg.replace('ON', colorize('ON', 'green'))
    if 'OFF' in msg:
        msg = msg.replace('OFF', colorize('OFF', 'red'))

    if color != 'default':
        box = f"[{colorize(type, color)}] {msg}"
    else:
        if type == 'info':
            box = f"[{colorize('INFO', 'cyan')}] {msg}"
        elif type == 'note':
            box = f"[{colorize('NOTE', 'yellow')}] {msg}"
        elif type == 'warn':
            box = f"[{colorize('WARN', 'red')}] {msg}"
        elif type == 'ok':
            box = f"[{colorize('OK', 'green')}] {msg}"
        elif type == 'add':
            box = f"[{colorize('ADD', 'green')}] {msg}"
        elif type == 'del':
            box = f"[{colorize('DEL', 'purple')}] {msg}"
    print(box)

def format_dt(string):
    """
    Formats datetime string to os appropriate format
    """
    if os.name == 'nt':
        return string.replace('-', '#')
    else:
        return string.replace('#', '-')

def time_obj(time):
    """
    Creates a time object with int or str
    """
    if isinstance(time, str) and not time.isdigit():
        try:
            return dt.strptime(time, '%H:%M').time()
        except ValueError:
            # print("[WARN] Time format should be HH:MM and from 0:00 to 23:59 when passing a str as argument")
            print_box("Time format should be HH:MM and from 0:00 to 23:59 when passing a str as argument", type='warn')
    elif isinstance(time, int) or (isinstance(time, str) and time.isdigit()):
        try:
            return dt.strptime(str(time), '%H').time()
        except ValueError:
            # print("[WARN] Time format should be H and from 0 to 23 when passing an int as argument")
            print_box("Time format should be H and from 0 to 23 when passing an int as argument", type='warn')
    elif isinstance(time, datetime.time):
        return time
    elif isinstance(time, datetime.datetime):
        return time.time()
    elif time is None:
        # print("[WARN] Must specify a time")
        print_box("Must specify a time", type='warn')
    else:
        print(time)
        # print(f"[WARN] {type(time).__name__.capitalize()} is not a valid argument for Time, it should be datetime.time, int or string")
        print_box("{type(time).__name__.capitalize()} is not a valid argument for Time, it should be datetime.time, int or string", type='warn')

def date_obj(somedate):
    """
    Creates a date object with int or str
    """
    if isinstance(somedate, str) and not somedate.isdigit():
        try:
            return dt.strptime(somedate, '%Y-%m-%d').date()
        except ValueError:
            # print("[WARN] Date format should be YYYY-MM-DD")
            print_box("Date format should be YYYY-MM-DD", type='warn')
    elif isinstance(somedate, int) or (isinstance(somedate, str) and somedate.isdigit()):
        try:
            return dt.now().date().replace(day=int(somedate))
        except ValueError:
            # print("[WARN] Date format should be D and the date must be valid when passing an int for the day")
            print_box("Date format should be D and the date must be valid when passing an int for the day", type='warn')
    elif type(somedate) == datetime.date:
        return somedate
    elif type(somedate) == datetime.datetime:
        return somedate.date()
    elif somedate is None:
        # print("[WARN] Must specify a date")
        print_box("Must specify a date", type='warn')
    else:
        # print(f"[WARN] {type(somedate).__name__.capitalize()} is not a valid argument for Date, it should be datetime.datetime, int or string")
        print_box("{type(somedate).__name__.capitalize()} is not a valid argument for Date, it should be datetime.datetime, int or string", type='warn')

def combine_date_time(date, time):
    try:
        return dt.combine(date, time)
    except ValueError:
        if not isinstance(date, datetime.date):
            raise ValueError("Date object is not valid")
        elif not isinstance(time, datetime.time):
            raise ValueError("Time object is not valid")
        else:
            raise ValueError("Something unexpected happened")

def weekend(date):
    """
    Checks if date object is on weekend
    """
    if date.weekday() > 4:
        return True
    return False

def first_weekday_x_months(weekends, **kwargs):
    """
    Returns the date with the first weekday of next X months
    """
    if 'date' not in kwargs:
        start_date = datetime.datetime.now().date()
    else:
        start_date = date_obj(kwargs['date'])

    months = 1
    if 'months' in kwargs:
        months = kwargs['months']

    start_month = start_date.month
    next_month = start_date.replace(month=start_month + months, day=1)

    if weekends:
        return next_month
    else:
        while True:
            if next_month.weekday() != 5 and next_month.weekday() != 6:
                return next_month
            else:
                next_month = next_month.replace(day=next_month.day+1)

def round_time(time, string='0m', tolerance=5):
    """
    Rounds time to next :30 or :00, always to ceiling with optional tolerance value, default is 5'
    """
    tolerance = abs(tolerance)
    time_object = time_obj(time)
    date_object = date_obj(datetime.datetime.now().date())
    date_combined = datetime.datetime.combine(date_object, time_object)

    hours = 0
    minutes = 0
    if 'm' in string and 'h' not in string:
        minutes = int(string.split('m')[:-1][0])
    if 'h' in string and 'm' not in string:
        hours = int(string.split('h')[:-1][0])
    if 'h' in string and 'm' in string:
        minutes = int(string.split('h')[1][:-1])
        hours = int(string.split('h')[0])

    date_combined = date_combined.replace(second=0, microsecond=0)
    date_combined = date_combined + datetime.timedelta(hours=hours, minutes=minutes)

    if 0 < date_combined.time().minute <= tolerance:
        date_combined = date_combined.replace(minute=0)
    elif 30 < date_combined.time().minute <= 30 + tolerance:
        date_combined = date_combined.replace(minute=30)

    while True:
        if date_combined.minute % 30 != 0:
            date_combined = date_combined + datetime.timedelta(minutes=1)
        else:
            return date_combined.time()

def relative_date(date):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    today = datetime.datetime.now().date()
    date = date_obj(date)
    rel_time = date - today
    if rel_time.days >= 0:
        if rel_time.days == 0:
            return "Today"
        elif rel_time.days == 1:
            return "Tomorrow"
        elif today.isocalendar()[1] == date.isocalendar()[1]:      ## it's the same week
            return f"on {days[date.weekday()]}"
        elif date.isocalendar()[1] - today.isocalendar()[1] == 1:  ## it's next week
            return f"next {days[date.weekday()]}"
        else:
            return f"on {date}"
    else:
        return f"on {date}"
    

def file_exists(file):
    return os.path.exists(file)


# def add_relative_time(string, tolerance=5):

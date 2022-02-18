from datetime import datetime

def time_obj(time):
    try:
        return datetime.strptime(time, '%H:%M').time()
    except ValueError:
        print("Time format should be HH:MM and from 0:00 to 23:59")
    except TypeError:
        print("Time must be a string")

def date_obj(date):
    try:
        return datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        print("Date format should be YYYY-MM-DD")

def combine_date_time(date, time):
    return datetime.combine(date, time)


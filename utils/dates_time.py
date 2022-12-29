import datetime
from pytz import timezone

# Set timezone
tz = timezone("Australia/Brisbane")

def get_nowutc():
    now = datetime.datetime.utcnow()
    return now

def get_now():
    now = datetime.datetime.now(tz).strftime("%H:%M:%S")
    return now
  
def get_today():
    today = datetime.datetime.now(tz).strftime("%d/%m")
    return today

def get_weekend():
    today = datetime.date.now(tz).weekday()
    if today == 5 or today == 6:
        return True
    else:
        return False

def get_tomorrow():
    today = datetime.date.today(tz)
    return today + datetime.timedelta(days=1)

def seconds_until(hours, minutes):
    given_time = datetime.time(hours, minutes)
    now = datetime.datetime.now()
    future_exec = datetime.datetime.combine(now, given_time)
    if (future_exec - now).days < 0: # If we are past the execution, it will take place tomorrow
        future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time) # days always >= 0
    return (future_exec - now).total_seconds()
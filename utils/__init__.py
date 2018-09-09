import json
from datetime import datetime, timedelta
import time

def load_file(file_name):
    return open('records/' + file_name)

def load_record_json(file_name):
    data_file = load_file(file_name)
    raw_data = data_file.read()
    data_file.close()
    try:
        return json.loads(raw_data)
    except JSONDecodeError as e:
        print('Couldn\'t parse record JSON')
        return None


#######################
# Time and Date Utils #
#######################
def timestamp_to_datetime(stamp, downgrade=False):
    if (downgrade):
        stamp = stamp / 1000
    time = int(stamp)
    return datetime.fromtimestamp(stamp)

def day_to_id(date):
    start_of_day = time.mktime(datetime(date.year, date.month, date.day).timetuple())
    return start_of_day

def is_within_days(date, days):
    delta = day_to_id(datetime.today()) - day_to_id(date)
    num_days = delta / (60*60*24)
    if num_days <= days:
        return True
    else:
        return False

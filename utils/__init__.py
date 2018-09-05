import json
from datetime import datetime, timedelta

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
def timestamp_to_datetime(stamp):
    time = (int) stamp
    return datetime.fromtimestamp(unix_ts)

def day_to_id(date):
    start_of_day = datetime(date.year, date.month, date.day)
    return start_of_day.timetuple()

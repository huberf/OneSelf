import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils

ENUMERATE = False

config = loadConfig.getConfig()

try:
    json_data = utils.load_record_json('nomie-backup.nomie.json')
except:
    print('Make sure you\'ve synced or exported your Nomie data')
    sys.exit()

trackers = json_data['trackers'] # Main keys: charge, config->uom, label, math (mean, etc.)

TRACKER_ID_TO_NAME = {}
for i in trackers:
    TRACKER_ID_TO_NAME[i['_id']] = i['label']

raw_events = json_data['events']

def tracker_id_to_name(id):
    try:
        return TRACKER_ID_TO_NAME[id]
    except:
        return None

def process_events(raw_events):
    to_return = []
    for i in raw_events:
        to_yield = {
                'tracker_id': i['parent'],
                'time': i['time']
                }
        try:
            to_yield['value'] = i['value']
        except:
            pass
        try:
            to_yield['geo'] = i['geo']
        except:
            pass
        # yield to_yield
        to_return += [to_yield]
    return to_return

events = process_events(raw_events)


def pretty_print_trackers():
    global trackers
    for i in trackers:
        try:
            if not i['config']['uom'] == None:
                print(i['label'], 'with type', i['config']['uom'])
            else:
                print(i['label'], 'with no defined type')
        except KeyError as e:
            print(i['label'])

if ENUMERATE:
    pretty_print_trackers()

def highest_trackers_used():
    global events, trackers, TRACKER_ID_TO_NAME
    tracker_map = {}
    for i in events:
        try:
            tracker_map[i['tracker_id']] += 1
        except:
            tracker_map[i['tracker_id']] = 1
    hit_list = []
    for i in tracker_map.keys():
        try:
            hit_list += [ [TRACKER_ID_TO_NAME[i], tracker_map[i]] ]
        except KeyError as e:
            pass # Tracker no longer exists
    return sorted(hit_list, key=lambda x: x[1], reverse=True)

recent_trackers = [
        'Water'
        ]
daily_expected = {
        'Water': {
            'val': 3.0, # 3 quarts
            'high': 5.0, # 1.8 times val
            'low': 1.5 # 0.8 times val
            }
        }

name = input("Tracker name to show results for: ")
val_sum = 0
day_vals = {}
for i in events:
    try:
        if TRACKER_ID_TO_NAME[i['tracker_id']] == name:
            log_time = i['time']
            date = utils.timestamp_to_datetime(log_time, True)
            day_id = utils.day_to_id(date)
            try:
                val = float(i['value'])
                if val == 0:
                    day_vals[day_id] += 1
                else:
                    day_vals[day_id] += float(i['value'])
            except:
                day_vals[day_id] = 0
    except KeyError:
        pass
avg_day = 0
maxi = None
mini = None
for i in day_vals.keys():
    if maxi == None or mini == None:
        maxi = day_vals[i]
        mini = day_vals[i]
    avg_day += day_vals[i]
    if maxi < day_vals[i]:
        maxi = day_vals[i]
    if mini > day_vals[i]:
        mini = day_vals[i]
avg_day /= len(day_vals.keys())
print("Avg per day: {0}".format(avg_day))
print("Max: {0}".format(maxi))
print("Min: {0}".format(mini))

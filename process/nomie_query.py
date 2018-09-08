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

def overview_report():
    tracker_counts = highest_trackers_used()
    print('Your most used trackers by count where {0}, {1}, {2}, {3} and {4}'.format(
        tracker_counts[0][0],
        tracker_counts[1][0],
        tracker_counts[2][0],
        tracker_counts[3][0],
        tracker_counts[4][0]
        ))

def recent_changes_report():
    global events, trackers, TRACKER_ID_TO_NAME
    water_items = []
    water_average = 0
    current_day = ''
    recent_days = {}
    water_average_pre = 0
    late_days = {}
    # Compatible trackers, Water in Ounces
    for i in events:
        # Water work
        if tracker_id_to_name(i['tracker_id']) == 'Water':
            water_items += [i]
            log_time = i['time']
            date = utils.timestamp_to_datetime(log_time, True)
            day_id = utils.day_to_id(date)
            val = int(i['value'])
            if utils.is_within_days(date, 7):
                try:
                    recent_days[day_id] += val
                except:
                    recent_days[day_id] = val
            else:
                try:
                    late_days[day_id] += val
                except:
                    late_days[day_id] = val
    length = len(recent_days.keys())
    for i in recent_days.keys():
        water_average += recent_days[i]
    if length > 0:
        water_average /= length
    length = len(late_days.keys())
    for i in late_days.keys():
        water_average_pre += late_days[i]
    if length > 0:
        water_average_pre /= length
    print('Recent average: ', water_average)
    print('Previous average: ', water_average_pre)
    pass

# Now Show Report
overview_report()
recent_changes_report()

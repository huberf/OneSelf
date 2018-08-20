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

def process_events(raw_events):
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
        yield to_yield

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


# Now Show Report
print('Your most used tracker by count was {0}'.format(highest_trackers_used()[0][0]))

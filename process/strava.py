# Standard imports. Add analysis specific ones.
import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator

config = loadConfig.getConfig()

# Load data
try:
    json_data = utils.load_record_json('strava-data.json')
except:
    print('Make sure you\'ve synced or exported your Strava data')
    sys.exit()

print(json_data['activities'][0].keys())

# TODO: Make difficulty metric based on things like heart rate and the nature of
# the elevation changes
lifetime_distance = 0
avg_hrs = []
# Main processing loop over all activities
for i in json_data['activities']:
    try:
        avg_hr = sum(i['heartrate'])/len(i['heartrate'])
        avg_hrs += [avg_hr]
    except KeyError:
        pass
    try:
        distance = i['distance'][-1]
        lifetime_distance += distance
    except:
        pass

hr_change = 0 # Change of first half of activities to next half
split = int(len(avg_hrs)/2)
first = sum(avg_hrs[:split])/len(avg_hrs[:split])
second = sum(avg_hrs[split:])/len(avg_hrs[split:])
hr_change = second - first

activity_count = len(json_data['activities'])
print('Activity Count:', activity_count)
print('Lifetime Distance:', lifetime_distance)
print('Lifetime HR Change:', hr_change)

parts = [
        ['header', ['Strava Report']],
        ['big_num', ['Activity Count', activity_count]],
        ['big_num', ['Lifetime Distance', lifetime_distance]],
        ['big_num', ['Lifetime HR Change', hr_change]]
        ]
generator.build_report('strava_main', parts)

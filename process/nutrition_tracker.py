# This script is intended to intelligently monitor your nutrition data
import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig

config = loadConfig.getConfig()

try:
    data_file = open('records/myfitnesspal-food.json')
    contents = data_file.read()
    json_data = json.loads(contents)
    data_file.close()
except:
    print('Make sure you\'ve synced MyFitnessPal nutrition data')
    sys.exit()

def current_health(data):
    day_data = data['data']
    top = len(day_data)
    bottom = len(day_data) - 8
    if bottom < 0:
        bottom = 0
    last_seven_days = day_data[bottom:top]
    # Check how you compare to recommended nutrient values
    calorie_sum = 0
    for i in last_seven_days:
        calorie_sum += i['day']['totals']['calories']
    days = top - bottom
    calorie_avg = calorie_sum / days
    print('You averaged {0} calories per day in the last week.'.format(calorie_avg))
    return

def recent_changes(data):
    return

def longterm_health(data):
    return

current_health(json_data)
recent_changes(json_data)
longterm_health(json_data)

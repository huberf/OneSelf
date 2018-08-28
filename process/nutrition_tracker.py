# This script is intended to intelligently monitor your nutrition data
import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils

config = loadConfig.getConfig()

try:
    json_data = utils.load_record_json('myfitnesspal-food.json')
except IOError as e:
    print('Make sure you\'ve synced MyFitnessPal nutrition data')
    sys.exit()

BASELINE_METRICS = {
    'calories': 2200,
    'carbohydrates': 300,
    'fat': 65,
    'protein': 50,
    'sodium': 2.4,
    'sugar': 0
}

def current_health(data):
    day_data = data['data']
    top = len(day_data)
    bottom = len(day_data) - 8
    if bottom < 0:
        bottom = 0
    last_seven_days = day_data[bottom:top]
    # Check how you compare to recommended nutrient values
    for j in BASELINE_METRICS.keys():
        value_sum = 0
        for i in last_seven_days:
            value_sum += i['day']['totals'][j]
        days = top - bottom
        value_avg = value_sum / days
        expected_intake = BASELINE_METRICS[j]
        if abs(0 if expected_intake == 0 else value_avg/expected_intake) > 2:
            print('RED ALERT: You averaged {0} {name} per day in the last week but expected to average {1}.'.format(value_avg, expected_intake, name=j))
        else:
            print('You averaged {0} {name} per day in the last week compared to expected {1}.'.format(value_avg, expected_intake, name=j))
    return

def recent_changes(data):
    day_data = data['data']
    top = len(day_data)
    bottom = len(day_data) - 8
    if bottom < 0:
        bottom = 0
    last_week = day_data[bottom:top]
    top = bottom
    bottom = top - 7*3
    if bottom < 0:
        bottom = 0
    three_weeks_before = day_data[bottom:top]
    recent_norms = {}
    historical_norms = {}
    for i in BASELINE_METRICS.keys():
        recent_norms[i] = 0
        historical_norms[i] = 0
    for i in last_week:
        for j in recent_norms.keys():
            recent_norms[j] += i['day']['totals'][j]
    for i in three_weeks_before:
        for j in historical_norms.keys():
            historical_norms[j] += i['day']['totals'][j]
    for i in recent_norms.keys():
        recently = recent_norms[i]/7.0
        historically = historical_norms[i]/(7.0*3)
        print('Recently you had {0} {1} vs. historically having {2}'.format(recently, i, historically))
    return

def longterm_health(data):
    return

current_health(json_data)
recent_changes(json_data)
longterm_health(json_data)

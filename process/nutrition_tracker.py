# This script is intended to intelligently monitor your nutrition data
import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator

config = loadConfig.getConfig()

html_parts = []
def add_message(text):
    global html_parts
    print(text)
    html_parts += [ ['paragraph', [text] ] ]


try:
    json_data = utils.load_record_json('myfitnesspal-food.json')
except IOError as e:
    print('Make sure you\'ve synced MyFitnessPal nutrition data')
    sys.exit()

BASELINE_METRICS = {
    'calories': 2200,
    'carbohydrates': 300,
    'fat': 65,
    'protein': 56,
    'sodium': 2400,
    'sugar': 50
}

def remove_untracked_days(days):
    to_return = []
    for i in days:
        if not i['day']['totals'] == {}:
            to_return += [i]
    return to_return

def current_health(data):
    day_data = data['data']
    top = len(day_data)
    bottom = len(day_data) - 8
    if bottom < 0:
        bottom = 0
    last_seven_days = remove_untracked_days(day_data[bottom:top])
    # Check how you compare to recommended nutrient values
    for j in BASELINE_METRICS.keys():
        value_sum = 0
        for i in last_seven_days:
            try:
                value_sum += i['day']['totals'][j]
            except KeyError:
                pass
        days = len(last_seven_days)
        value_avg = value_sum / days
        expected_intake = BASELINE_METRICS[j]
        if abs(0 if expected_intake == 0 else value_avg/expected_intake) > 2:
            add_message('RED ALERT: You averaged {0} {name} per day in the last week but expected to average {1}.'.format(value_avg, expected_intake, name=j))
        else:
            add_message('You averaged {0:.1f} {name} per day in the last week compared to expected {1:.1f}.'.format(value_avg, expected_intake, name=j))
    return

def recent_changes(data):
    day_data = data['data']
    top = len(day_data)
    bottom = len(day_data) - 8
    if bottom < 0:
        bottom = 0
    last_week = remove_untracked_days(day_data[bottom:top])
    top = bottom
    bottom = top - 7*3
    if bottom < 0:
        bottom = 0
    three_weeks_before = remove_untracked_days(day_data[bottom:top])
    recent_norms = {}
    historical_norms = {}
    for i in BASELINE_METRICS.keys():
        recent_norms[i] = 0
        historical_norms[i] = 0
    for i in last_week:
        for j in recent_norms.keys():
            try:
                recent_norms[j] += i['day']['totals'][j]
            except KeyError:
                pass
    for i in three_weeks_before:
        for j in historical_norms.keys():
            try:
                historical_norms[j] += i['day']['totals'][j]
            except KeyError:
                pass
    for i in recent_norms.keys():
        recently = recent_norms[i]/len(last_week)
        historically = historical_norms[i]/len(three_weeks_before)
        add_message('Recently you had {0:.1f} {1} vs. historically having {2:.1f}'.format(recently, i, historically))
    return

def longterm_health(data):
    day_data = data['data']
    bottom = len(day_data) - 365
    if bottom < 0:
        bottom = 0
    top = len(day_data)
    last_year = day_data[bottom:top]
    year_norms = {}
    for i in BASELINE_METRICS.keys():
        year_norms[i] = 0
    last_year = remove_untracked_days(last_year)
    for i in last_year:
        for j in year_norms.keys():
            try:
                year_norms[j] += i['day']['totals'][j]
            except KeyError:
                pass # Normal for day to not have some values
    num_entries = len(last_year)
    for i in year_norms.keys():
        year_day_avg = year_norms[i]/num_entries
        add_message('Year average for {0} is {1:.1f}'.format(i, year_day_avg))
    return

current_health(json_data)
recent_changes(json_data)
longterm_health(json_data)

# Now generate HTML report
parts = [
        ['header', ['Nutrition Report']],
        ]
parts += html_parts
generator.build_report('nutrition_main', parts)

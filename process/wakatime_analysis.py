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
    json_data = utils.load_record_json('wakatime-export.json')
except:
    print('Make sure you\'ve synced or exported your WakaTime')
    sys.exit()

def calc_top_languages(days):
    language_hours = {}
    for i in days:
        for lang in i['languages']:
            try:
                language_hours[lang['name']] += lang['total_seconds']
            except:
                language_hours[lang['name']] = lang['total_seconds']
    sorted_list = sorted(language_hours.items(), key=lambda kv: kv[1])
    sorted_list.reverse()
    return sorted_list

def calc_total_time(days):
    total_time = 0 # in seconds
    for i in days:
        total_time += i['grand_total']['total_seconds']
    return total_time

print(json_data['days'][0]['grand_total'].keys())
# Gather overall metrics
total_time = calc_total_time(json_data['days']) # in seconds
languages = calc_top_languages(json_data['days'])
print('Total Hours:', total_time/(60*60))
print('All-Time Top Languages: 1)', languages[0][0], '2)', languages[1][0])


# Gather last month metrics
num_days = len(json_data['days'])
total_time = calc_total_time(json_data['days'][num_days-31:num_days])
languages = calc_top_languages(json_data['days'][num_days-31:num_days])
print('Last Month Hours:', total_time/(60*60))
print('Last Month Top Languages: 1)', languages[0][0], '2)', languages[1][0])

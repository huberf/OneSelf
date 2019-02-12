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

def most_edited_files(days):
    file_hours = {}
    for j in days:
        for k in j['projects']:
            for i in k['entities']:
                try:
                    file_hours[i['name']] += i['total_seconds']
                except:
                    file_hours[i['name']] = i['total_seconds']
    sorted_list = sorted(file_hours.items(), key=lambda kv: kv[1])
    sorted_list.reverse()
    return sorted_list

def weekend_weekday_percentage(days):
    weekend_time = 0
    weekday_time = 0
    for i in days:
        date = i['date']
        vals = date.split('-')
        year = int(vals[0])
        month = int(vals[1])
        day = int(vals[2])
        if datetime.datetime(year, month, day).weekday() > 4:
            weekend_time += i['grand_total']['total_seconds']
        else:
            weekday_time += i['grand_total']['total_seconds']
    if not weekday_time == 0:
        return weekend_time/(weekday_time+weekend_time)
    else:
        return -1

print(json_data['days'][0]['grand_total'].keys())
# Gather overall metrics
num_days = len(json_data['days'])
total_time = calc_total_time(json_data['days']) # in seconds
languages = calc_top_languages(json_data['days'])
print('Total Hours:', total_time/(60*60))
print('All-Time Top Languages: 1)', languages[0][0], '2)', languages[1][0])
bottom = num_days-365
if bottom < 0:
    bottom = 0
print('Hours Last Year:', calc_total_time(json_data['days'][bottom:num_days])/(60*60))

top_langs_html = ['top3', ['All Time Top Languages',
    languages[0][0] if len(languages) > 0 else "None",
    languages[1][0] if len(languages) > 1 else "None",
    languages[2][0] if len(languages) > 2 else "None"]]


# Gather last month metrics
total_time = calc_total_time(json_data['days'][num_days-31:num_days])
languages = calc_top_languages(json_data['days'][num_days-31:num_days])
last_month_hours = total_time/(60*60)
print('Last Month Hours:', last_month_hours)
print('Last Month Top Languages: 1)', languages[0][0], '2)', languages[1][0])
try:
    most_edited_file_this_month = most_edited_files(json_data['days'][num_days-31:num_days])[0][0]
except:
    most_edited_file_this_month = "None"
print('Most Edited File This Month:', most_edited_file_this_month)
print('Weekend Coding Percentage: {0:.2f}%'.format(weekend_weekday_percentage(json_data['days'][num_days-31:num_days])*100))

top_langs_month_html = ['top3', ['Last Month Top Languages',
    languages[0][0] if len(languages) > 0 else "None",
    languages[1][0] if len(languages) > 1 else "None",
    languages[2][0] if len(languages) > 2 else "None"]]
# Now generate HTML report
parts = [
        ['header', ['Wakatime Report']],
        ['big_num', ['Last Month Hours', last_month_hours]],
        ['big_num', ['Mosted Edited File This Month', most_edited_file_this_month]],
        top_langs_html,
        top_langs_month_html
        ]
generator.build_report('wakatime_main', parts)

import sys
import datetime
import json
import csv
import os
from os import path
import numpy as np
sys.path.append( path.dirname( path.dirname( path.dirname( path.abspath(__file__) ) ) ) )
from utils import loadConfig
import utils
import generator

config = loadConfig.getConfig()

def check_aggregates_directory():
    directory = 'aggregates/'
    if not os.path.exists(directory):
        os.makedirs(directory)

check_aggregates_directory()

print('Last.fm...')
try:
    song_data = utils.load_record_json('lastfm-data.json')
    song_days = {}
    for i in song_data['data']:
        timestamp = i['date']['uts']
        date = datetime.datetime.utcfromtimestamp(float(timestamp))
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_timestamp = date.timestamp()
        try:
            song_days[day_timestamp] += [i]
        except:
            song_days[day_timestamp] = [i]
    day_blocks = []
    for i in song_days.keys():
        block = {
                'timestamp': i,
                'songCount': 0
                }
        block['songCount'] = len(song_days[i])
        day_blocks += [block]
    csv_contents = ''
    for i in day_blocks:
        csv_contents += '{0},{1}\n'.format(i['timestamp'], i['songCount'])
    out_file = open('aggregates/day_blocks_song_count.csv', 'w')
    out_file.write(csv_contents)
    out_file.close()
except FileNotFoundError:
    print('Not set up.')

print('RescueTime...')
def load_rescuetime_data():
    data_file = utils.load_file('rescuetime-data.csv')
    data_reader = csv.reader(data_file)
    keys = ['timestamp', 'name', 'details', 'type', 'subclass', 'val']
    records = []
    for row in data_reader:
        record = { }
        for i,val in enumerate(keys):
            if val == 'val':
                record[val] = int(row[i])
            else:
                record[val] = row[i]
        records += [record]
    return { 'records': records }
try:
    computer_data = load_rescuetime_data()
    computer_days = {}
    for i in computer_data['records']:
        date = i['timestamp']
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z")
        date_obj = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        timestamp = int(date_obj.timestamp())
        try:
            computer_days[timestamp] += [i]
        except:
            computer_days[timestamp] = [i]
    day_blocks = []
    for i in computer_days.keys():
        block = {
                'timestamp': i,
                'computerScore': 0
                }
        try:
            computer_data = computer_days[i]
            for comp in computer_data:
                block['computerScore'] += comp['val']
        except KeyError:
            pass
        day_blocks += [block]
    csv_contents = ''
    for i in day_blocks:
        csv_contents += '{0},{1}\n'.format(i['timestamp'], i['computerScore'])
    out_file = open('aggregates/day_blocks_rescuetime_val_sum.csv', 'w')
    out_file.write(csv_contents)
    out_file.close()
except FileNotFoundError:
    print('Not set up.')

print('Gyroscope...')
all_export_files = os.listdir('records/gyroscope/')
# Load all day HR data
hr_files = []
for i in all_export_files:
    beginning_indicator = 'gyroscope-Noah-hr-export'
    if i[:len(beginning_indicator)] == beginning_indicator:
        hr_files += [i]
hr_data = []
times_added = {}
for i in hr_files:
    csv_data = open('records/gyroscope/' + i, 'r')
    data_reader = csv.reader(csv_data)
    first_row = True
    for row in data_reader:
        if first_row:
            first_row = False
            continue
        try: # Verify this is a new time
            times_added[row[0]]
        except KeyError:
            row_data = {
                    'time': row[0],
                    'bpm': int(row[1]),
                    'service': row[2]
                    }
            times_added[row[0]] = True
            hr_data += [row_data]
heart_rate_days = {}
for i in hr_data:
    date = i['time']
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d-%H:%M:%S")
    date_obj = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp = int(date_obj.timestamp())
    try:
        heart_rate_days[timestamp] += [i]
    except:
        heart_rate_days[timestamp] = [i]
day_blocks = []
for i in heart_rate_days.keys():
    block = {
            'timestamp': i,
            'avgHr': 0
            }
    try:
        vals = heart_rate_days[i]
        for comp in vals:
            block['avgHr'] += comp['bpm']
        block['avgHr'] /= len(vals) # Convert to avg
    except KeyError:
        pass
    day_blocks += [block]
csv_contents = ''
for i in day_blocks:
    csv_contents += '{0},{1}\n'.format(i['timestamp'], i['avgHr'])
out_file = open('aggregates/day_blocks_gyroscope_avg_hr.csv', 'w')
out_file.write(csv_contents)
out_file.close()

print('MyFitnessPal...')
try:
    json_data = utils.load_record_json('myfitnesspal-food.json')
    METRICS = ['calories', 'carbohydrates', 'fat', 'protein', 'sodium', 'sugar']
    day_data = json_data['data']
    calorie_days = {}
    nutrition_days = {
            'calories': {},
            'carbohydrates': {},
            'fat': {},
            'protein': {},
            'sodium': {},
            'sugar': {}
            }
    for i in day_data:
        date = i['date']
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_obj = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        timestamp = int(date_obj.timestamp())
        for metric in METRICS:
            try:
                nutrition_days[metric][timestamp] += [i['day']['totals'][metric]]
            except:
                try:
                    nutrition_days[metric][timestamp] = [i['day']['totals'][metric]]
                except:
                    nutrition_days[metric][timestamp] = [0]
    day_blocks = []
    for i in nutrition_days['calories'].keys():
        block = {
                'timestamp': i,
                'calories': 0,
                'carbohydrates': 0,
                'fat': 0,
                'protein': 0,
                'sodium': 0,
                'sugar': 0
                }
        for metric in METRICS:
            try:
                nutrition_data = nutrition_days[metric][i]
                for comp in nutrition_data:
                    block[metric] += comp
            except KeyError:
                pass
        day_blocks += [block]
    for metric in METRICS:
        csv_contents = ''
        for i in day_blocks:
            csv_contents += '{0},{1}\n'.format(i['timestamp'], i[metric])
        out_file = open('aggregates/day_blocks_{0}_sum.csv'.format(metric), 'w')
        out_file.write(csv_contents)
        out_file.close()
except FileNotFoundError:
    print('Not set up.')

print('Garmin...')
def load_garmin_data():
    data_file = utils.load_file('garmin-activities.csv')
    data_reader = csv.reader(data_file)
    transaction_data = []
    first_row = True
    activities = []
    for row in data_reader:
        if first_row:
            first_row = False
            continue
        # Keys: Activity Type,Date,Favorite,Title,Distance,Calories,Time,Avg HR,Max HR,Avg Run Cadence,Max Run Cadence,Avg Pace,Best Pace,Elev Gain,Elev Loss,Avg Stride Length,Avg Vertical Ratio,Avg Vertical Oscillation,
        # Training Stress Score®,Grit,Flow,Total Strokes,Avg. Swolf,Avg Stroke Rate,Bottom Time,Min Water Temp,Surface Interval,Decompression
        keys = [
                'type', 'date', 'favorite', 'title', 'distance', 'calories',
                'time', 'avg_hr', 'max_hr', 'avg_cadence', 'max_cadence',
                'avg_pace', 'best_pace', 'elev_gain', 'elev_loss', 'avg_stride_length',
                'avg_vertical_ratio', 'avg_vertical_oscillation', 'training_stress_score',
                'grit', 'flow', 'total_strokes', 'avg_swolf', 'avg_stroke_rate',
                'bottom_time', 'min_water_temp', 'surface_interval', 'decompression'
                ]
        activity = { }
        for i,val in enumerate(keys):
            activity[val] = row[i]
        activities += [activity]
    return { 'activities': activities }
try:
    activity_data = load_garmin_data()
    acitivity_days = {}
    for i in activity_data['activities']:
        date = i['date']
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_obj = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        timestamp = int(date_obj.timestamp())
        try:
            activity_days[timestamp] += [i]
        except:
            activity_days[timestamp] = [i]
    day_blocks = []
    for i in activity_days.keys():
        block = {
                'timestamp': i,
                'calories': 0,
                'avg_hr': 0,
                'distance': 0,
                'avg_cadence': 0,
                'elev_gain': 0
                }
        try:
            activity_data = activity_days[i]
            for comp in activity_data:
                block['calories'] += comp['calories']
                block['avg_hr'] += comp['avg_hr']
                block['distance'] += comp['distance']
                block['avg_cadence'] += comp['avg_cadence']
                block['elev_gain'] += comp['elev_gain']
        except KeyError:
            pass
        day_blocks += [block]
    csv_contents = ''
    for i in day_blocks:
        csv_contents += '{0},{1}\n'.format(i['timestamp'], i['calories'])
    out_file = open('aggregates/day_blocks_garmin_calories_sum.csv', 'w')
    out_file.write(csv_contents)
    out_file.close()
except FileNotFoundError:
    print('Not set up.')

print('Done.')

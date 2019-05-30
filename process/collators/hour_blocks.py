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
    song_hours = {}
    for i in song_data['data']:
        timestamp = i['date']['uts']
        date = datetime.datetime.utcfromtimestamp(float(timestamp))
        date = date.replace(minute=0, second=0, microsecond=0)
        hour_timestamp = date.timestamp()
        try:
            song_hours[hour_timestamp] += [i]
        except:
            song_hours[hour_timestamp] = [i]
    hour_blocks = []
    for i in song_hours.keys():
        block = {
                'timestamp': i,
                'songCount': 0
                }
        block['songCount'] = len(song_hours[i])
        hour_blocks += [block]
    csv_contents = ''
    for i in hour_blocks:
        csv_contents += '{0},{1}\n'.format(i['timestamp'], i['songCount'])
    out_file = open('aggregates/hour_blocks_song_count.csv', 'w')
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
    computer_hours = {}
    for i in computer_data['records']:
        date = i['timestamp']
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z")
        date_obj = date_obj.replace(minute=0, second=0, microsecond=0)
        timestamp = int(date_obj.timestamp())
        try:
            computer_hours[timestamp] += [i]
        except:
            computer_hours[timestamp] = [i]
    hour_blocks = []
    for i in computer_hours.keys():
        block = {
                'timestamp': i,
                'computerScore': 0
                }
        try:
            computer_data = computer_hours[i]
            for comp in computer_data:
                block['computerScore'] += comp['val']
        except KeyError:
            pass
        hour_blocks += [block]
    csv_contents = ''
    for i in hour_blocks:
        csv_contents += '{0},{1}\n'.format(i['timestamp'], i['computerScore'])
    out_file = open('aggregates/hour_blocks_rescuetime_val_sum.csv', 'w')
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
heart_rate_hours = {}
for i in hr_data:
    date = i['time']
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d-%H:%M:%S")
    date_obj = date_obj.replace(minute=0, second=0, microsecond=0)
    timestamp = int(date_obj.timestamp())
    try:
        heart_rate_hours[timestamp] += [i]
    except:
        heart_rate_hours[timestamp] = [i]
hour_blocks = []
for i in heart_rate_hours.keys():
    block = {
            'timestamp': i,
            'avgHr': 0
            }
    try:
        vals = heart_rate_hours[i]
        for comp in vals:
            block['avgHr'] += comp['bpm']
        block['avgHr'] /= len(vals) # Convert to avg
    except KeyError:
        pass
    hour_blocks += [block]
csv_contents = ''
for i in hour_blocks:
    csv_contents += '{0},{1}\n'.format(i['timestamp'], i['avgHr'])
out_file = open('aggregates/hour_blocks_gyroscope_avg_hr.csv', 'w')
out_file.write(csv_contents)
out_file.close()

print('Done.')

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

print('Done.')

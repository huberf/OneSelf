# This is an experimental script to try to do inference between
# songs listened and computer productivity.
import sys
import datetime
import json
import csv
from os import path
import numpy as np
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator

config = loadConfig.getConfig()

print('Loading data...')

# LOAD SONG DATA
try:
    song_data = utils.load_record_json('lastfm-data.json')
except:
    print('Make sure you\'ve synced or exported your last.fm data')
    sys.exit()

# LOAD COMPUTER USE DATA
def load_data():
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
    computer_data = load_data()
except:
    print('Make sure you\'ve synced or exported your Rescuetime data')
    sys.exit()

print('Data loaded. Beginning processing...')

print('Indexing all data to hours...')
computer_hours = {}
for i in computer_data['records']:
    date = i['timestamp']
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z")
    date_obj = date_obj.replace(minute=0, second=0)
    timestamp = int(date_obj.timestamp())
    try:
        computer_hours[timestamp] += [i]
    except:
        computer_hours[timestamp] = [i]
song_hours = {}
for i in song_data['data']:
    timestamp = i['date']['uts']
    date = datetime.datetime.utcfromtimestamp(float(timestamp))
    date = date.replace(minute=0, second=0)
    hour_timestamp = date.timestamp()
    try:
        song_hours[timestamp] += [i]
    except:
        song_hours[timestamp] = [i]

# IDEA: Box work into hours with songCount and workType
print('Computer hour blocks: {0}'.format(len(computer_hours.keys())))
print('Song hour blocks: {0}'.format(len(song_hours.keys())))

print('Crunching hour blocks')

hour_blocks = []
for i in song_hours.keys():
    block = {
            'songCount': 0,
            'computerScore': 0
            }
    try:
        computer_data = computer_hours[i]
        for comp in computer_data:
            block['computerScore'] += comp['val']
        print('Found computer')
    except KeyError:
        pass
    block['songCount'] = len(song_hours[i])
    hour_blocks += [block]

print(list(song_hours.keys())[0])
print(list(computer_hours.keys())[0])

relation = np.corrcoef(list(i['songCount'] for i in hour_blocks), list(i['computerScore'] for i in hour_blocks))
print(relation)

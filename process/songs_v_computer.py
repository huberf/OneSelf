# This is an experimental script to try to do inference between
# songs listened and computer productivity.
import sys
import datetime
import json
import csv
from os import path
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
''computer_hours = {}
for i in computer_data['records']:
    date = i['timestamp']
    timestamp = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z").timestamp()
    try:
        computer_hours[timestamp] += [i]
    except:
        computer_hours[timestamp] = [i]
song_hours = {}
for i in song_data['data']:
    timestamp = i['date']['uts']
    date = datetime.utcfromtimestamp(float(timestamp))
    date.hours = 0
    date.seconds = 0
    hour_timestamp = date.timestamp()
    try:
        song_hours[timestamp] += [i]
    except:
        song_hours[timestamp] = [i]

# IDEA: Box work into hours with songCount and workType
hour_blocks = []
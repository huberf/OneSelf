import sys
import datetime
import json
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
print('Done.')

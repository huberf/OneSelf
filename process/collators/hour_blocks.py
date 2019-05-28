import sys
import datetime
import json
from os import path
import numpy as np
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator

config = loadConfig.getConfig()

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
    csv_contents = ''
    for i in song_data.keys():
        csv_contents += '{0},{1}\n'.format(i, song_data[i])
    out_file = open('aggregates/hour_blocks_song_count.csv', 'w')
    out_file.write(csv_contents)
except:
    print('Not set up.')
print('Done.')

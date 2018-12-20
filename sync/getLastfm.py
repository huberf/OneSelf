import json
import sys
from os import path
import datetime
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils.loadConfig as loadConfig

from lastpy import extras

config = loadConfig.getConfig()

user_name = config['keys']['lastfm']['username']

sync_back_days = 600

def save(data):
    to_save = { 'data': data, 'lastsave': str(datetime.datetime.now()) }
    save_file = open('records/lastfm-data.json', 'w')
    save_file.write(json.dumps(to_save, indent=4))
    save_file.close()

data = []

for i in range(0, sync_back_days):
    print('Saving day {0} of {1}'.format(i, sync_back_days))
    back_days = sync_back_days - i
    tracks = extras.user_daily_tracks(user_name, back_days)
    data += tracks['recenttracks']['track']

print('Saving data...')
save(data)
print('Data saved.')

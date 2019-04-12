import json
import sys
import os
from os import path
import requests as r
import datetime
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils.loadConfig as loadConfig

from lastpy import extras

config = loadConfig.getConfig()

api_root = 'http://ws.audioscrobbler.com/2.0/'

user_name = config['keys']['lastfm']['username']

sync_back_days = 1200

def user_back_tracks(user_name, days_back=0, limit=200, page=1):
    dayStart = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=-days_back)
    dayStart = dayStart.strftime('%s')
    resp = r.get(api_root + '?method=user.getrecenttracks&user=' + user_name + '&api_key=' + os.environ['LAST_FM_API'] + '&from=' + str(dayStart) + '&limit=' + str(limit) +'&format=json')
    conts = json.loads(resp.text)
    total_pages = conts['recenttracks']['@attr']['totalPages']
    print('There are {0} pages to download'.format(total_pages))
    tracks = []
    for i in range(0, int(total_pages)):
        print('Syncing page {0} of {1}'.format(i+1, total_pages))
        downloaded = False
        to_add = []
        while not downloaded:
            try:
                resp = r.get(api_root + '?method=user.getrecenttracks&user=' + user_name + '&api_key=' + os.environ['LAST_FM_API'] + '&from=' + str(dayStart) + '&limit=' + str(limit) +'&page=' + str(i+1) +'&extended=1&format=json')
                conts = json.loads(resp.text)
                to_add = conts['recenttracks']['track']
                downloaded = True # Quit the loop
            except Exception as e:
                print('Retrying after error {0}'.format(e))
        tracks += to_add
        # Backing up in case of crash
        save(tracks)
    return tracks

def save(data):
    to_save = { 'data': data, 'lastsave': str(datetime.datetime.now()) }
    save_file = open('records/lastfm-data.json', 'w')
    save_file.write(json.dumps(to_save, indent=4))
    save_file.close()

data = []

data = user_back_tracks(user_name, sync_back_days)
print(data)

print('Saving data...')
save(data)
print('Data saved.')

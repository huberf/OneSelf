import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils.loadConfig

from stravalib.client import Client
from stravalib import unithelper
from utils import loadConfig

config = loadConfig.getConfig()

user_name = config['keys']['strava']['username']
access_token = None
athlete_id = None
try:
    access_token = config['keys']['strava']['access_token']
    athlete_id = config['keys']['strava']['runner_id']
except:
    # No access token. Failing.
    print('Make sure you have your access token and athelete ID setup per the instructions in the README')
    sys.exit()

class StravaData:
    RUNNER_ID = None
    ACCESS_TOKEN = None
    client = None
    def __init__(self, runner_id, access_token):
        self.RUNNER_ID = runner_id
        self.ACCESS_TOKEN = access_token
        self.client = Client()
        self.client.access_token = access_token

    def getAthlete(self):
        athlete = self.client.get_athlete()
        return athlete

    def getActivities(self):
        activities = self.client.get_activities()
        return activities

    def getActivity(self, id):
        activity = self.client.get_activity(id)
        return activity

    def getActivityStreams(self, id, types):
        streams = self.client.get_activity_streams(id, types=types, resolution='medium')
        return streams

data_proxy = StravaData(athlete_id, access_token)

athlete_data = data_proxy.getAthlete()
activities = data_proxy.getActivities()
print(activities)
print(athlete_data)
to_save = {
        'activities': [],
        'id': athlete_data.id,
        'first_name': athlete_data.firstname,
        'last_name': athlete_data.lastname,
        'count': 0
        }

already_processed = {}
try:
    save_file = open('records/strava-data.json')
    save_data = json.loads(save_file.read())
    to_save = save_data
    save_file.close()
    for i in save_data['activities']:
        already_processed[i['id']] = True
except:
    pass

def save(data):
    save_file = open('records/strava-data.json', 'w')
    save_file.write(json.dumps(data, indent=4))
    save_file.close()

activities_packaged = []
record = 1
for i in activities:
    print('Processing activity {0}'.format(record))
    try:
        already_processed[i.id] # If this succeeds it's already processed
    except:
        activity = data_proxy.getActivity(i.id)
        types = ['time', 'latlng', 'altitude', 'heartrate', 'temp']
        streams = data_proxy.getActivityStreams(i.id, types)
        to_add = {
                'id': i.id,
                'name': i.name,
                'distance': float(unithelper.miles(activity.distance)),
                'date': str(i.start_date)
                }
        for i in streams:
            try:
                to_add[i] = streams[i].data
            except:
                print('No {0} data for this activity'.format(i))
        to_save['activities'] += [to_add]
        to_save['count'] = len(to_save['activities'])
        save(to_save)
    record += 1


print('Saving...')
print(to_save)
save(to_save)
print('Done.')

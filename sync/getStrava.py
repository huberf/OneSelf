import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils.loadConfig

from stravalib.client import Client
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

data_proxy = StravaData(athlete_id, access_token)

athlete_data = data_proxy.getAthlete()
activities = data_proxy.getActivities()
print(athlete_data)
for i in activities:
    print(i)

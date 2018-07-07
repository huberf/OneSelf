import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils.loadConfig

from stravalib.client import Client
from utils import loadConfig

config = loadConfig.getConfig()

client = Client()
user_name = config['keys']['strava']['username']
access_token = None
try:
    access_token = config['keys']['strava']['access_token']
    athlete_id = config['keys']['strava']['athlete_id']
    client.access_token = access_token
except:
    # No access token. Failing.
    print('Make sure you have your access token and athelete ID setup per the instructions in the README")

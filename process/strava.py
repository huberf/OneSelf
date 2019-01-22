# Standard imports. Add analysis specific ones.
import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator

config = loadConfig.getConfig()

# Load data
try:
    json_data = utils.load_record_json('strava-data.json')
except:
    print('Make sure you\'ve synced or exported your Strava data')
    sys.exit()

activity_count = len(json_data['activities'])
print('Activity Count:', activity_count)

parts = [
        ['header', ['Strava Report']],
        ['big_num', ['Activity Count', activity_count]]
        ]
generator.build_report('strava_main', parts)

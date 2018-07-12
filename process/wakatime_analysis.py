# This script is intended to intelligently monitor your nutrition data
import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig

config = loadConfig.getConfig()

try:
    data_file = open('records/wakatime-export.json')
    contents = data_file.read()
    json_data = json.loads(contents)
    data_file.close()
except:
    print('Make sure you\'ve synced or exported your WakaTime')
    sys.exit()

print(json_data['days'][0]['grand_total'].keys())
# Gather overall metrics
total_time = 0 # in seconds
for i in json_data['days']:
    total_time += i['grand_total']['total_seconds']
print('Total Hours:', total_time/(60*60))

# Gather last month metrics
num_days = len(json_data['days'])
total_time = 0
for i in json_data['days'][num_days-31:num_days]:
    total_time += i['grand_total']['total_seconds']
print('Last Month Hours:', total_time/(60*60))

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

try:
    json_data = utils.load_record_json('swarm-checkins.json')
except:
    print('Make sure you\'ve synced or exported your Swarm data')
    sys.exit()

# Main processing loop
for i,val in enumerate(json_data['checkins']['items']):
    pass

checkin_total = json_data['checkins']['count']
print('Total check-ins:', checkin_total)

parts = [
        ['header', ['Swarm Report']],
        ['big_num', ['Check-in Count', checkin_total]]
        ]
generator.build_report('swarm_main', parts)

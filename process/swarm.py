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

print('Total check-ins:', json_data['checkins']['count'])

parts = [
        ['header', ['Swarm Report']],
        ['big_num', ['Check-in Count', json_data['checkins']['count']]]
        ]
generator.build_report('swarm_main', parts)

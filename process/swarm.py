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

zipcode_count = {}

# Main processing loop
for i,val in enumerate(json_data['checkins']['items']):
    try:
        zipcode_count[val['venue']['location']['postalCode']] += 1
    except:
        try:
            zipcode_count[val['venue']['location']['postalCode']] = 1
        except:
            pass # Doesn't have zipcode
    pass

top_zipcodes = sorted(zipcode_count.items(), key=lambda kv:kv[1])
top_zipcodes.reverse()
topzips_html = generator.build_top3('Top Zipcodes', top_zipcodes, True)

checkin_total = json_data['checkins']['count']
print('Total check-ins:', checkin_total)

parts = [
        ['header', ['Swarm Report']],
        ['big_num', ['Check-in Count', checkin_total]],
        topzips_html
        ]
generator.build_report('swarm_main', parts)

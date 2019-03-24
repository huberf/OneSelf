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
places_count = {}
state_count = {}

#print(json_data['checkins']['items'][0])

# Main processing loop
for i,val in enumerate(json_data['checkins']['items']):
    #print(val)
    try:
        zipcode_count[val['venue']['location']['postalCode']] += 1
    except:
        try:
            zipcode_count[val['venue']['location']['postalCode']] = 1
        except:
            pass # Doesn't have zipcode
    try:
        state_count[val['venue']['location']['state']] += 1
    except:
        try:
            state_count[val['venue']['location']['state']] = 1
        except:
            pass # Doesn't have state
    try:
        places_count[val['venue']['name']] += 1
    except:
        try:
            places_count[val['venue']['name']] = 1
        except:
            pass # Doesn't have name
    pass

def get_top_entry(dictionary, name):
    top = sorted(dictionary.items(), key=lambda kv:kv[1])
    top.reverse()
    return generator.build_top3(name, top, True)

topzips_html = get_top_entry(zipcode_count, 'Top Zipcodes')
topstates_html = get_top_entry(state_count, 'Top States')
topplaces_html = get_top_entry(places_count, 'Top Places')

checkin_total = json_data['checkins']['count']
print('Total check-ins:', checkin_total)

parts = [
        ['header', ['Swarm Report']],
        ['big_num', ['Check-in Count', checkin_total]],
        topzips_html,
        topstates_html,
        topplaces_html
        ]
generator.build_report('swarm_main', parts)

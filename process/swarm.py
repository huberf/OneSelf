# Standard imports. Add analysis specific ones.
import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator
try:
    HAS_SENTIMENT = True
    from utils import sentiment
except ImportError:
    HAS_SENTIMENT = False

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

shout_sentiments = []
# Main processing loop
for i,val in enumerate(json_data['checkins']['items']):
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
    if HAS_SENTIMENT:
        try:
            post_sentiment = sentiment.assess(val['shout'])
            shout_sentiments += [post_sentiment['compound']]
        except KeyError:
            pass

if HAS_SENTIMENT:
    avg_sentiment = sum(shout_sentiments)/len(shout_sentiments)
    sentiment_html = ['big_num', ['Average Shout Sentiment', '{:.1f}% positive'.format(avg_sentiment*100)]]
else:
    sentiment_html = ['big_num', ['Average Shout Sentiment', 'Not configured']]


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
        sentiment_html,
        topzips_html,
        topstates_html,
        topplaces_html
        ]
generator.build_report('swarm_main', parts)

import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator

ENUMERATE = False

config = loadConfig.getConfig()

try:
    json_data = utils.load_record_json('nomie-backup.nomie.json')
except:
    print('Make sure you\'ve synced or exported your Nomie data')
    sys.exit()

trackers = json_data['trackers'] # Main keys: charge, config->uom, label, math (mean, etc.)

TRACKER_ID_TO_NAME = {}
for i in trackers:
    TRACKER_ID_TO_NAME[i['_id']] = i['label']

raw_events = json_data['events']

def tracker_id_to_name(id):
    try:
        return TRACKER_ID_TO_NAME[id]
    except:
        return None

def process_events(raw_events):
    to_return = []
    for i in raw_events:
        to_yield = {
                'tracker_id': i['parent'],
                'time': i['time']
                }
        try:
            to_yield['value'] = i['value']
        except:
            pass
        try:
            to_yield['geo'] = i['geo']
        except:
            pass
        # yield to_yield
        to_return += [to_yield]
    return to_return

events = process_events(raw_events)


def pretty_print_trackers():
    global trackers
    for i in trackers:
        try:
            if not i['config']['uom'] == None:
                print(i['label'], 'with type', i['config']['uom'])
            else:
                print(i['label'], 'with no defined type')
        except KeyError as e:
            print(i['label'])

if ENUMERATE:
    pretty_print_trackers()

def highest_trackers_used():
    global events, trackers, TRACKER_ID_TO_NAME
    tracker_map = {}
    for i in events:
        try:
            tracker_map[i['tracker_id']] += 1
        except:
            tracker_map[i['tracker_id']] = 1
    hit_list = []
    for i in tracker_map.keys():
        try:
            hit_list += [ [TRACKER_ID_TO_NAME[i], tracker_map[i]] ]
        except KeyError as e:
            pass # Tracker no longer exists
    return sorted(hit_list, key=lambda x: x[1], reverse=True)

def overview_report():
    tracker_counts = highest_trackers_used()
    print('Your most used trackers by count where {0}, {1}, {2}, {3} and {4}'.format(
        tracker_counts[0][0],
        tracker_counts[1][0],
        tracker_counts[2][0],
        tracker_counts[3][0],
        tracker_counts[4][0]
        ))

recent_trackers = [
        'Water'
        ]
daily_expected = {
        'Water': {
            'val': 3.0, # 3 quarts
            'high': 5.0, # 1.8 times val
            'low': 1.5 # 0.8 times val
            }
        }
def recent_changes_report():
    global events, trackers, TRACKER_ID_TO_NAME
    global recent_trackers, daily_expected
    water_average = 0
    average = {}
    for i in recent_trackers:
        average[i] = 0
    recent_days = {}
    for i in recent_trackers:
        recent_days[i] = {}
    average_pre = {}
    for i in recent_trackers:
        average_pre[i] = 0
    late_days = {}
    for i in recent_trackers:
        late_days[i] = {}
    # Compatible trackers, Water in Ounces
    for i in events:
        # Water work
        for j in recent_trackers:
            if tracker_id_to_name(i['tracker_id']) == j:
                log_time = i['time']
                date = utils.timestamp_to_datetime(log_time, True)
                day_id = utils.day_to_id(date)
                val = int(i['value'])
                if utils.is_within_days(date, 7):
                    try:
                        recent_days[j][day_id] += val
                    except:
                        recent_days[j][day_id] = val
                else:
                    try:
                        late_days[j][day_id] += val
                    except:
                        late_days[j][day_id] = val
    # Water
    for j in recent_trackers:
        length = len(recent_days[j].keys())
        for i in recent_days[j].keys():
            average[j] += recent_days[j][i]
        if length > 0:
            average[j] /= length
        fraction_off_perfection = average[j] / daily_expected[j]['val']
        if (average[j] < daily_expected[j]['low']):
            print('WARNING: {name} is just {percent}% of recommendation this week'.format(name=j, percent=fraction_off_perfection*100))
        if (average[j] > daily_expected[j]['high']):
            print('WARNING: {name} is {percent}% more than recommended this week'.format(name=j, percent=fraction_off_perfection*100))
        length = len(late_days[j].keys())
        for i in late_days[j].keys():
            average_pre[j] += late_days[j][i]
        if length > 0:
            average_pre[j] /= length
        historical_change = average[j] / average_pre[j]
        if (historical_change < 0.5 or historical_change > 1.5):
            print('WARNING: {name} has changed by {value} times.'.format(name=j, value=historical_change))
        print('{name} recent average: {avg}'.format(name=j, avg=average[j]))
        print('{name} previous average: {avg}'.format(name=j, avg=average_pre[j]))
    pass

goal_parts = []
def goals():
    global events, trackers, TRACKER_ID_TO_NAME
    global recent_trackers, daily_expected
    global goal_parts
    year_goals = [{
            'tracker': 'Push-ups',
            'avg': 40 # Per day
            }]
    sums = {}
    for i in events:
        # Water work
        for j in year_goals:
            if tracker_id_to_name(i['tracker_id']) == j['tracker']:
                log_time = i['time']
                date = utils.timestamp_to_datetime(log_time, True)
                val = int(i['value'])
                current_year = datetime.datetime.now().year
                days = (datetime.date.today() - datetime.date(current_year, 1, 1)).days
                if date.year == current_year:
                    try:
                        sums[j['tracker']] += val
                    except:
                        sums[j['tracker']] = val
    for i in sums.keys():
        for j in year_goals:
            if j['tracker'] == i:
                print('Averaged {0} {1} compared to expected {2}'.format(
                    sums[i]/days,i,j['avg']))
                goal_parts += [['subheader', ['{0} Goal Progress'.format(i)]],
                        ['completion_bar', [sums[i]/days, j['avg']]]]

# Now Show Report
overview_report()
recent_changes_report()
goals()

# Now generate HTML report
parts = [
        ['header', ['Nomie Report']],
        ]
parts += goal_parts
generator.build_report('nomie_query_main', parts)

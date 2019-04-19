import sys
import datetime
import json
from os import path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator
from matplotlib.dates import YearLocator
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator

ENUMERATE = False

print('Reading in data...')
config = loadConfig.getConfig()

try:
    json_data = utils.load_record_json('lastfm-data.json')
except:
    print('Make sure you\'ve synced or exported your last.fm data')
    sys.exit()

print('Processing data...')
songs_recorded = len(json_data['data'])
#songs_recorded = 0
artist_hits = {}
song_hits = {}
songs_per_day = {}
songs_per_year = {}
songs_per_month = {}
songs_per_weekday = {}
weekend_avg = 0
weekend_count = 0
weekday_avg = 0
weekday_count = 0
last_day = None
for j in json_data['data']:
    #songs_recorded += len(i)
    #for j in i:
    date = utils.timestamp_to_datetime(int(j['date']['uts']))
    day_of_week = date.weekday()
    if day_of_week == 5 or day_of_week == 6: # Weekend
        weekend_avg += 1
        if not last_day == date.strftime('%Y-%m-%d'):
            weekend_count += 1
    else:
        weekday_avg += 1
        if not last_day == date.strftime('%Y-%m-%d'):
            weekday_count += 1
    try:
        songs_per_year[date.year] += 1
    except:
        songs_per_year[date.year] = 1

    try:
        songs_per_month[date.month] += 1
    except:
        songs_per_month[date.month] = 1

    try:
        songs_per_weekday[date.weekday()] += 1
    except:
        songs_per_weekday[date.weekday()] = 1

    try:
        artist = j['artist']['name']
        try:
            artist_hits[artist] += 1
        except:
            artist_hits[artist] = 1
        try:
            song_hits[(j['name'], artist)] += 1
        except:
            song_hits[(j['name'], artist)] = 1
    except KeyError:
        pass
    last_day = date.strftime('%Y-%m-%d')

weekday_avg = weekday_avg / weekday_count
weekend_avg = weekend_avg / weekend_count
print('Weekday Average:', weekday_avg)
print('Weekend Average:', weekend_avg)

top_years = sorted(songs_per_year.items(), key=lambda kv:kv[1])
top_years.reverse()

top_artists = sorted(artist_hits.items(), key=lambda kv: kv[1])
top_artists.reverse()

top_songs = sorted(song_hits.items(), key=lambda kv: kv[1])
top_songs.reverse()
top_songs_html_info = ['Top Songs',
        '{0} by {1}'.format(top_songs[0][0][0], top_songs[0][0][1]),
        '{0} by {1}'.format(top_songs[1][0][0], top_songs[1][0][1]),
        '{0} by {1}'.format(top_songs[2][0][0], top_songs[2][0][1]),
        '{0} by {1}'.format(top_songs[3][0][0], top_songs[3][0][1]),
        '{0} by {1}'.format(top_songs[4][0][0], top_songs[4][0][1])
        ]


print("Songs recorded: {0}".format(songs_recorded))

print('Generating report...')

# Generate scrobbles per year graphic
year_xs = np.arange(len(songs_per_year.keys()))
plt.bar(year_xs, songs_per_year.values())
plt.xticks(year_xs, songs_per_year.keys())
plt.savefig('html/figures/lastfm_scrobble_years.png', dpi=200)
plt.close()

month_xs = np.arange(len(songs_per_month.keys()))
plt.bar(month_xs, songs_per_month.values())
plt.xticks(month_xs, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.savefig('html/figures/lastfm_scrobble_month.png', dpi=200)
plt.close()

weekday_xs = np.arange(len(songs_per_weekday.keys()))
plt.bar(weekday_xs, songs_per_weekday.values())
plt.xticks(weekday_xs, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
plt.savefig('html/figures/lastfm_scrobble_weekday.png', dpi=200)
plt.close()

# Now generate HTML report
parts = [
        ['header', ['Last.fm Report']],
        ['big_num', ['Songs recorded', songs_recorded]],
        ['big_num', ['Top Year', top_years[0][0]]],
        ['big_num', ['Weekend Average Count', weekend_avg]],
        ['big_num', ['Weekday Average Count', weekday_avg]],
        generator.build_top3('Top Artists', top_artists),
        ['top5', top_songs_html_info],
        ['subheader', ['Scrobbles Per Year']],
        ['image', ['figures/lastfm_scrobble_years.png']],
        ['subheader', ['Scrobbles Per Month']],
        ['image', ['figures/lastfm_scrobble_month.png']],
        ['subheader', ['Scrobbles Per Weekday']],
        ['image', ['figures/lastfm_scrobble_weekday.png']]
        ]
generator.build_report('lastfm_main', parts)
print('Done.')

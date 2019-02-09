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
    json_data = utils.load_record_json('lastfm-data.json')
except:
    print('Make sure you\'ve synced or exported your last.fm data')
    sys.exit()

#songs_recorded = len(json_data['data'])
songs_recorded = 0
artist_hits = {}
song_hits = {}
songs_per_day = {}
songs_per_year = {}
for i in json_data['data']:
    songs_recorded += len(i)
    for j in i:
        date = utils.timestamp_to_datetime(int(j['date']['uts']))
        try:
            songs_per_year[date.year] += 1
        except:
            songs_per_year[date.year] = 1

        artist = j['artist']['#text']
        try:
            artist_hits[artist] += 1
        except:
            artist_hits[artist] = 1
        try:
            song_hits[(j['name'], artist)] += 1
        except:
            song_hits[(j['name'], artist)] = 1

top_artists = sorted(artist_hits.items(), key=lambda kv: kv[1])
top_artists.reverse()

top_songs = sorted(song_hits.items(), key=lambda kv: kv[1])
top_songs.reverse()
top_songs_html_info = ['Top Songs',
        '{0} by {1}'.format(top_songs[0][0][0], top_songs[0][0][1]),
        '{0} by {1}'.format(top_songs[1][0][0], top_songs[1][0][1]),
        '{0} by {1}'.format(top_songs[2][0][0], top_songs[2][0][1])
        ]

print("Songs recorded: {0}".format(songs_recorded))


# Now generate HTML report
parts = [
        ['header', ['Last.fm Report']],
        ['big_num', ['Songs recorded', songs_recorded]],
        ['top3', ['Top Artists', top_artists[0][0], top_artists[1][0], top_artists[2][0]]],
        ['top3', top_songs_html_info]
        ]
generator.build_report('lastfm_main', parts)

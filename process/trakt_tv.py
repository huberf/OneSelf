import sys
from os import path
import datetime
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils
import utils.loadConfig

import csv

def load_data():
    data_file = utils.load_file('trakt-data.csv')
    data_reader = csv.reader(data_file)
    record_data = []
    first_row = True
    for row in data_reader:
        if first_row:
            first_row = False
            continue
        # Headers: watched_at,action,type,title,year,trakt_rating,trakt_id,imdb_id,
        # tmdb_id,tvdb_id,url,released,runtime,season_number,episode_number,
        # episode_title,episode_released,episode_trakt_rating,episode_trakt_id,
        # episode_imdb_id,episode_tmdb_id,episode_tvdb_id,genres
        record = {
            'watched_at': row[0],
            'action': row[1],
            'type': row[2],
            'title': row[3],
            'year': row[4],
            'trakt_rating': row[5],
            'trakt_id': row[6],
            'imdb_id': row[7],
            'tmdb_id': row[8] # TODO: Add more
            }
        record_data += [record]
    return { 'records': record_data }

data = load_data()

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
            'tmdb_id': row[8],
            'tvdb_id': row[9],
            'url': row[10],
            'released': row[11],
            'runtime': float(row[12]) # TODO: Add more
            }
        record_data += [record]
    return { 'records': record_data }

def year_avg_watchtime(data, just_tv=False):
    total_time = 0
    current = datetime.datetime.now()
    for i in data['records']:
        if (not just_tv or i['type'] == 'episode'):
            if i['watched_at'][0:4] == str(datetime.datetime.now().year):
                total_time += i['runtime']
    days = (datetime.date.today() - datetime.date(current.year, 1, 1)).days
    average_per_day = float(total_time) / days
    hours_per_day = average_per_day/60
    return hours_per_day

def top_shows(data, mode='watchtime'):
    show_to_weight = {}
    if mode == 'watchtime':
        for i in data['records']:
            if i['type'] == 'episode':
                try:
                    show_to_weight[i['title']] += i['runtime']
                except:
                    show_to_weight[i['title']] = i['runtime']
    sorted_list = sorted(show_to_weight.items(), key=lambda kv: kv[1])
    sorted_list.reverse()
    return sorted_list

data = load_data()
print('Average Watchtime Per Day (Past Year): {0:.2f}'.format(year_avg_watchtime(data)))
print('Average TV Watchtime Per Day (Past Year): {0:.2f}'.format(year_avg_watchtime(data, True)))
show_list = top_shows(data, 'watchtime')
print('Top Shows:\n\t1) {0} at {1:.1f} hours\n\t2) {2} at {3:.1f} hours\n\t3) {4} at {5:.2f} hours'.format(
    show_list[0][0], show_list[0][1]/60, show_list[1][0], show_list[1][1]/60, show_list[2][0], show_list[2][1]/60
))

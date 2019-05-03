import sys
from os import path
import datetime
import matplotlib.pyplot as plt
import numpy as np
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils
import utils.loadConfig
import generator

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

def avg_watchtimes(data, just_tv=False):
    watchtime_per_weekday = {}
    watchtime_per_month = {}
    watchtime_per_year = {}
    for i in data['records']:
        if (not just_tv or i['type'] == 'episode'):
            date_obj = datetime.datetime.strptime(i['watched_at'], '%Y-%m-%dT%H:%M:%SZ')
            try:
                watchtime_per_weekday[date_obj.weekday()] += i['runtime']
            except:
                watchtime_per_weekday[date_obj.weekday()] = i['runtime']

            try:
                watchtime_per_month[date_obj.month] += i['runtime']
            except:
                watchtime_per_month[date_obj.month] = i['runtime']

            try:
                watchtime_per_year[date_obj.year] += i['runtime']
            except:
                watchtime_per_year[date_obj.year] = i['runtime']

    weekday_xs = np.arange(len(watchtime_per_weekday.keys()))
    plt.bar(weekday_xs, watchtime_per_weekday.values())
    plt.xticks(weekday_xs, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.savefig('html/figures/trakt_watchtime_weekday.png', dpi=200)
    plt.close()

    month_xs = np.arange(len(watchtime_per_month.keys()))
    plt.bar(month_xs, watchtime_per_month.values())
    plt.xticks(month_xs, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.savefig('html/figures/trakt_watchtime_month.png', dpi=200)
    plt.close()

    year_xs = np.arange(len(watchtime_per_year.keys()))
    plt.bar(year_xs, watchtime_per_year.values())
    plt.xticks(year_xs, watchtime_per_year.keys())
    plt.savefig('html/figures/trakt_watchtime_years.png', dpi=200)
    plt.close()


def year_avg_watchtime(data, just_tv=False, year=None):
    current_year = datetime.datetime.now().year
    if year == None:
        year = current_year
    total_time = 0
    current = datetime.datetime.now()
    for i in data['records']:
        if (not just_tv or i['type'] == 'episode'):
            if i['watched_at'][0:4] == str(year):
                total_time += i['runtime']
    if year == current_year:
        days = (datetime.date.today() - datetime.date(current.year, 1, 1)).days
    else:
        days = 365 # Leap years exist but not a big difference
    if days > 0:
        average_per_day = float(total_time) / days
    else:
        average_per_day = 0
    hours_per_day = average_per_day/60
    return hours_per_day

def avg_watchtime_all_years(data):
    curr_year = datetime.datetime.now().year
    to_return = {}
    while curr_year > 2000:
        avg_all = year_avg_watchtime(data, False, curr_year)
        if avg_all > 0:
            to_return[curr_year] = {
                    'avg_all': avg_all,
                    'avg_tv': year_avg_watchtime(data, True, curr_year)
                    }
        curr_year -= 1
    return to_return

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

avg_watchtimes(data)

val_year_avg_watchtime = year_avg_watchtime(data)
print('Average Watchtime Per Day (Past Year): {0:.2f}'.format(val_year_avg_watchtime))
val_year_avg_tv_watchtime = year_avg_watchtime(data, True)
print('Average TV Watchtime Per Day (Past Year): {0:.2f}'.format(val_year_avg_tv_watchtime))
show_list = top_shows(data, 'watchtime')
print('Top Shows:\n\t1) {0} at {1:.1f} hours\n\t2) {2} at {3:.1f} hours\n\t3) {4} at {5:.2f} hours'.format(
    show_list[0][0], show_list[0][1]/60, show_list[1][0], show_list[1][1]/60, show_list[2][0], show_list[2][1]/60
))

avg_all_years = avg_watchtime_all_years(data)

year_avg_parts = []
for i in avg_all_years.keys():
    year_result = [ ['subheader', [i]], ['big_num', ['Average Watchtime Per Day', avg_all_years[i]['avg_all']]],
            ['big_num', ['Average TV Watchtime Per Day', avg_all_years[i]['avg_tv']]]]
    generator.check_html_directory('trakt')
    generator.build_report('trakt/{0}report'.format(i), year_result)
    year_avg_parts += year_result
    year_avg_parts += [ ['link', ['trakt/{0}report.html'.format(i), '{0} Full Report'.format(i)]] ]

# Now generate HTML report
parts = [
        ['header', ['Trakt.tv Report']],
        ['top3', ['Top Shows', show_list[0][0], show_list[1][0], show_list[2][0]]]
        ]
parts += year_avg_parts
parts += [
            ['subheader', ['Watchtime Per Weekday']],
            ['image', ['figures/trakt_watchtime_weekday.png']],
            ['subheader', ['Watchtime Per Month']],
            ['image', ['figures/trakt_watchtime_month.png']],
            ['subheader', ['Watchtime Per Year']],
            ['image', ['figures/trakt_watchtime_years.png']]
        ]
generator.build_report('trakttv_main', parts)

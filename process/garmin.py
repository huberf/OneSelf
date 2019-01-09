# Standard imports. Add analysis specific ones.
import sys
import datetime
import json
from os import path
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator
from matplotlib.dates import YearLocator
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator

config = loadConfig.getConfig()

import csv

def load_data():
    data_file = utils.load_file('garmin-activities.csv')
    data_reader = csv.reader(data_file)
    transaction_data = []
    first_row = True
    activities = []
    for row in data_reader:
        if first_row:
            first_row = False
            continue
        # Keys: Activity Type,Date,Favorite,Title,Distance,Calories,Time,Avg HR,Max HR,Avg Run Cadence,Max Run Cadence,Avg Pace,Best Pace,Elev Gain,Elev Loss,Avg Stride Length,Avg Vertical Ratio,Avg Vertical Oscillation,
        # Training Stress Score®,Grit,Flow,Total Strokes,Avg. Swolf,Avg Stroke Rate,Bottom Time,Min Water Temp,Surface Interval,Decompression
        keys = [
                'type', 'date', 'favorite', 'title', 'distance', 'calories',
                'time', 'avg_hr', 'max_hr', 'avg_cadence', 'max_cadence',
                'avg_pace', 'best_pace', 'elev_gain', 'elev_loss', 'avg_stride_length',
                'avg_vertical_ratio', 'avg_vertical_oscillation', 'training_stress_score',
                'grit', 'flow', 'total_strokes', 'avg_swolf', 'avg_stroke_rate',
                'bottom_time', 'min_water_temp', 'surface_interval', 'decompression'
                ]
        activity = { }
        for i,val in enumerate(keys):
            activity[val] = row[i]
        activities += [activity]
    return { 'activities': activities }

data = load_data()

# Graph average running pace
x = []
y = []
for i in data['activities']:
    if i['type'] == 'running':
        x += [i['date']]
        y += [i['avg_pace']]
#plt.plot(x, y)
ax = plt.subplot()
#ax.plot(x, y)
ax.yaxis.set_major_locator(HourLocator())
ax.yaxis.set_major_formatter(DateFormatter('%M:%s'))
ax.xaxis_date()
ax.xaxis.set_major_locator(YearLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
plt.plot(x, y)
generator.check_figure_directory()
plt.savefig('html/figures/garmin_total_avg_running_pace.png', dpi=400)
plt.close()

parts = [
        ['header', ['Garmin Report']],
        ['subheader', ['Average Running Pace']],
        ['image', ['figures/garmin_total_avg_running_pace.png']]
        ]
generator.build_report('garmin_main', parts)

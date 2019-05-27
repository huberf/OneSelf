# Standard imports. Add analysis specific ones.
import sys
import datetime
import csv
import json
from os import path
import os
import matplotlib.pyplot as plt
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator

config = loadConfig.getConfig()
#############
# Load data #
#############
all_export_files = os.listdir('records/gyroscope/')
# Load all day HR data
hr_files = []
for i in all_export_files:
    beginning_indicator = 'gyroscope-Noah-hr-export'
    if i[:len(beginning_indicator)] == beginning_indicator:
        hr_files += [i]
hr_data = []
times_added = {}
for i in hr_files:
    csv_data = open('records/gyroscope/' + i, 'r')
    data_reader = csv.reader(csv_data)
    first_row = True
    for row in data_reader:
        if first_row:
            first_row = False
            continue
        try: # Verify this is a new time
            times_added[row[0]]
        except KeyError:
            row_data = {
                    'time': row[0],
                    'bpm': int(row[1]),
                    'service': row[2]
                    }
            times_added[row[0]] = True
            hr_data += [row_data]

################
# Analyze Date #
################
lowest_hr = 250 # If this is too a cap, you are not a human
highest_hr = 0 # Sorry, highest can't be negative
each_hr_count = {}
for i in hr_data:
    if i['bpm'] < lowest_hr:
        lowest_hr = i['bpm']
    if i['bpm'] > highest_hr:
        highest_hr = i['bpm']
    try:
        each_hr_count[i['bpm']] += 1
    except KeyError:
        each_hr_count[i['bpm']] = 1

avg_hr = sum(list(i['bpm'] for i in hr_data))/len(hr_data)

print('Heart Rate Points: {0}'.format(len(hr_data)))
print('Highest HR:', highest_hr)
print('Lowest HR:', lowest_hr)

plt.scatter(each_hr_count.keys(), each_hr_count.values())
plt.xlabel('BPM')
plt.ylabel('Count')
plt.savefig('html/figures/gyroscope_hr_scatter.png', dpi=200)
plt.close()

parts = [
        ['header', ['Gyroscope Report']],
        ['subheader', ['Heart Rate Analysis']],
        ['big_num', ['Highest HR', highest_hr]],
        ['big_num', ['Lowest HR', lowest_hr]],
        ['big_num', ['Average HR', avg_hr]],
        ['image', ['figures/gyroscope_hr_scatter.png']]
        ]
generator.build_report('gyroscope_main', parts)

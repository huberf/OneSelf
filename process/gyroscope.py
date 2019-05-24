# Standard imports. Add analysis specific ones.
import sys
import datetime
import csv
import json
from os import path
import os
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
                    'bpm': row[1],
                    'service': row[2]
                    }
            times_added[row[0]] = True
            hr_data += [row_data]

print('Heart Rate Points: {0}'.format(len(hr_data)))

parts = [
        ['header', ['Gyroscope Report']],
        ]
generator.build_report('gyroscope_main', parts)

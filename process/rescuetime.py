import sys
from os import path
import datetime
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils
import utils.loadConfig
import generator

import csv

def load_data():
    data_file = utils.load_file('rescuetime-data.csv')
    data_reader = csv.reader(data_file)
    keys = ['timestamp', 'name', 'details', 'type', 'subclass', 'val']
    records = []
    for row in data_reader:
        record = { }
        for i,val in enumerate(keys):
            if val == 'val':
                record[val] = int(row[i])
            else:
                record[val] = row[i]
        records += [record]
    return { 'records': records }

data = load_data()

application_hits = {}
# General Data Processing
for i in data['records']:
    try:
        application_hits[i['name']] += i['val']
    except:
        application_hits[i['name']] = i['val']

top_applications = sorted(application_hits.items(), key=lambda kv: kv[1])
top_applications.reverse()

print('Generating report...')
# Now generate HTML report
parts = [
        ['header', ['RescueTime Report']],
        ['top3', ['Top Applications', top_applications[0][0], top_applications[1][0], top_applications[2][0]]],
        ]
generator.build_report('rescuetime_main', parts)

print('Done.')

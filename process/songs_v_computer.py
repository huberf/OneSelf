# This is an experimental script to try to do inference between
# songs listened and computer productivity.
import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator

config = loadConfig.getConfig()

# LOAD SONG DATA
try:
    json_data = utils.load_record_json('lastfm-data.json')
except:
    print('Make sure you\'ve synced or exported your last.fm data')
    sys.exit()

# LOAD COMPUTER USE DATA
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

try:
    data = load_data()
except:
    print('Make sure you\'ve synced or exported your Rescuetime data')
    sys.exit()

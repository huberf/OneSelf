import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils.loadConfig

import myfitnesspal
from utils import loadConfig

config = loadConfig.getConfig()

user_name = config['keys']['myfitnesspal']['username']
client = myfitnesspal.Client(user_name)

to_save = {
        'data': [],
        'count': 0
        }

try:
    data_file = open('records/myfitnesspal-food.json')
    contents = data_file.read()
    json_data = json.loads(contents)
    to_save = json_data
    data_file.close()
except:
    pass

lastSync = datetime.datetime(2018, 6, 28)
current = lastSync
today = datetime.datetime.now()
while current <= today:
  print('Syncing data for {0}'.format(current))
  day = client.get_date(current.year, current.month, current.day)
  breakfast = day.meals[0]
  lunch = day.meals[1]
  dinner = day.meals[2]
  current += datetime.timedelta(days=1)
  new_entry = {
      'date': current.strftime("%Y-%m-%d %H:%M:%S"),
      'day': {
          'totals': day.totals
          },
      'breakfast': {
          'totals': breakfast.totals,
          'entries': breakfast.entries
          },
      'lunch': {
          'totals': lunch.totals,
          'entries': lunch.entries
          },
      'dinner': {
          'totals': dinner,
          'entires': dinner.entries
          }
      }
  to_save['data'] += [new_entry]
  to_save['count'] += 1

data_file = open('records/myfitnesspal-food.json', 'w')
data_file.write(json.dumps(to_save))
data_file.close()


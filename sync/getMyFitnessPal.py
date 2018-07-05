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

lastSync = datetime.datetime.strptime(
            config['keys']['myfitnesspal']['last_sync'],
            '%Y-%m-%d'
        )
current = lastSync
today = datetime.datetime.now()
while current < today:
  print('Syncing data for {0}'.format(current))
  day = client.get_date(current.year, current.month, current.day)
  breakfast = day.meals[0]
  lunch = day.meals[1]
  dinner = day.meals[2]
  empty = False
  if day.totals == 0:
      empty = True
  new_entry = {
      'date': current.strftime("%Y-%m-%d %H:%M:%S"),
      'empty': empty,
      'day': {
          'totals': day.totals
          },
      'breakfast': {
          'totals': breakfast.totals,
          'entries': []
          },
      'lunch': {
          'totals': lunch.totals,
          'entries': []
          },
      'dinner': {
          'totals': dinner.totals,
          'entries': []
          }
      }
  for i in breakfast.entries:
      new_entry['breakfast']['entries'] += [{
          'name': i.name,
          'totals': i.totals
          }]
  for i in lunch.entries:
      new_entry['lunch']['entries'] += [{
          'name': i.name,
          'totals': i.totals
          }]
  for i in dinner.entries:
      new_entry['dinner']['entries'] += [{
          'name': i.name,
          'totals': i.totals
          }]
  to_save['data'] += [new_entry]
  to_save['count'] += 1
  current += datetime.timedelta(days=1)

print('Displaying contents to save in case of crash:')
print(to_save)

data_file = open('records/myfitnesspal-food.json', 'w')
data_file.write(json.dumps(to_save))
data_file.close()
# Write new last sync date
lastSync = current.strftime('%Y-%m-%d')
config['keys']['myfitnesspal']['last_sync'] = lastSync
loadConfig.setConfig(config)

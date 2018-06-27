import sys
import datetime
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

lastSync = datetime.datetime(2013, 3, 2)
current = lastSync
today = datetime.datetime.now()
while current <= today:
  day = client.get_date(current.year, current.month, current.day)
  breakfast = day.meals[0]
  lunch = day.meals[1]
  dinner = day.meals[2]
  current += datetime.timedelta(days=1)
  to_save['data'] += [{
      'date': current,
      'breakfast': breakfast,
      'lunch': lunch,
      'dinner': dinner
      }]
  to_save['count'] += 1

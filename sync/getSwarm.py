import json, requests
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils.loadConfig

from utils import loadConfig

config = loadConfig.getConfig()

client_id = config['keys']['foursquare']['client_id']
client_secret = config['keys']['foursquare']['client_secret']
access_code = config['keys']['foursquare']['access_code']

url = 'https://api.foursquare.com/v2/users/self/checkins'

params = dict(
  client_id=client_id,
  client_secret=client_secret,
  oauth_token=access_code,
  v='20180323',
  limit=250
)
resp = requests.get(url=url, params=params)
data = json.loads(resp.text)

data_file = open('records/swarm-checkins.json', 'w')
data_file.write(json.dumps(data['response']))
data_file.close()

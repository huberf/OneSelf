import requests as r
import time
import datetime
import json

STEP_GOAL = 10000

config = json.load(open('config.json', 'r'))
username = config['username']

daily_summary_url = 'https://connect.garmin.com/modern/proxy/usersummary-service/usersummary/daily/{username}?calendarDate={date}'

curr_date = str(datetime.datetime.now())[:10]
garmin_data = json.loads(r.get(daily_summary_url.format(username=username, date=curr_date)).text)
curr_steps = garmin_data['totalSteps']

if curr_steps < STEP_GOAL:
    r.post(config['failure_url'], { 'value1': curr_steps })

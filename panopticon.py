# This file is meant to routinely run and track report files and update the user with
# any changes
import subprocess
from time import sleep

reports = [
        'mint_finance',
        'nomie_query',
        'nutrition_tracker',
        'wakatime_analysis'
        ]

responses_library = {}

def analyze_report(report_name):
    text = subprocess.check_output(['python3', 'process/{name}.py'.format(name=report_name)])
    lines = text.split(b'\n')
    for i in lines:
        try:
            responses_library[i]
        except:
            print('{0}'.format(i))
            responses_library[i] = 0

def check_reports():
    for i in reports:
        analyze_report(i)

ticks = 0
while True:
    ticks += 1
    print('Running #{0}'.format(ticks))
    check_reports()

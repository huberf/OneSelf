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

def show_update(updated_line):
    print(updated_line)

def analyze_report(report_name):
    global responses_library
    text = subprocess.check_output(['python3', 'process/{name}.py'.format(name=report_name)])
    lines = text.split(b'\n')
    for i in lines:
        try:
            responses_library[i]
            responses_library[i] = 0
        except:
            show_update(i)
            responses_library[i] = 0

def clean_old_responses():
    global responses_library
    for i in list(responses_library.keys()):
        if responses_library[i] > 0:
            del responses_library[i]
        else:
            responses_library[i] += 1

def check_reports():
    for i in reports:
        analyze_report(i)
    clean_old_responses()

ticks = 0
while True:
    ticks += 1
    print('Running #{0}'.format(ticks))
    check_reports()

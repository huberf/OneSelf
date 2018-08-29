import os
import requests as r

def url_encode(string):
    # Cleanup later maybe with external library
    return string.replace('/', '%2F').replace(' ', '%20').replace('#', '%23')


class Nomie:
    api_head = 'https://maker.ifttt.com/trigger/'
    api_key = os.environ['IFTTT_KEY']
    event_key = os.environ['IFTTT_MAKER_EVENT']
    replacements = {}

    def __init__(self, replacements):
        self.replacements = replacements

    def sendTracker(self, tracker_name, value):
        final_tracker = tracker_name
        try:
            final_tracker = replacements[tracker_name]
        except:
            do_nothing = True
        url_to_hit = self.api_head + self.event_key + '/with/key/' + api_key
        r.post(url_to_hit, { 'value1': final_tracker, 'value2': value })

    def sendNote(self, text):
        url_to_hit = self.api_head + self.event_key + '/with/key/' + api_key
        r.post(url_to_hit, { 'value1': 'note', 'value2': text })

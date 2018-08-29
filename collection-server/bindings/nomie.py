import os
import requests as r

def url_encode(string):
    # Cleanup later maybe with external library
    return string.replace('/', '%2F').replace(' ', '%20').replace('#', '%23')


class Nomie:
    api_head = 'https://api.nomie.io/v2/'
    api_key = os.environ['NOMIE_API_KEY']
    replacements = {}

    def __init__(self, replacements):
        self.replacements = replacements

    def sendTracker(self, tracker_name, value):
        final_tracker = tracker_name
        try:
            final_tracker = replacements[tracker_name]
        except:
            do_nothing = True
        cleaned_tracker = url_encode(final_tracker)
        url_to_hit = self.api_head + 'push/' + self.api_key + '/action=track/label=' + cleaned_tracker
        if not value == None:
            url_to_hit += '/value=' + value
        r.get(url_to_hit)

    def sendNote(self, text):
        cleaned_text = url_encode(text)
        url_to_hit = self.api_head + 'push/' + self.api_key + '/action=create-note/note=' + cleaned_text
        r.get(url_to_hit)

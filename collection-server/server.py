import os
import json
from flask import Flask
from flask import request
import requests as r
app = Flask(__name__)

replacements = {}
try:
    # Replacements change arbitrary tracker labels to a supplied subsitution
    # Allows one to make disparate namings function
    replacements = json.loads(open('replacements.json').read())
except:
    # Failed loading replacements
    replacements = {}

# Import bindings to various services
from bindings import nomie
myNomie = nomie.Nomie(replacements)

# Prepare security
auth_key = os.environ['PROXY_KEY']

@app.route("/")
def main():
    return "Server is functioning."

@app.route('/<auth_input>/<tracker_name>', defaults={'value': None})
@app.route("/<auth_input>/<tracker_name>/<value>")
def h(auth_input, tracker_name, value):
    success = True
    if auth_input == auth_key:
        try:
            myNomie.sendTracker(tracker_name, value)
        except:
            success = False
    else:
        success = False
    if success:
        return '{"success": "true"}'
    else:
        return '{"success": "false"}'

@app.route('/note/<auth_input>/<text>')
def note(auth_input, text):
    success = True
    if auth_input == auth_key:
        try:
            myNomie.sendNote(text)
        except:
            success = False
    if success:
        return '{"success": "true"}'
    else:
        return '{"success": "false"}'

# Nomie 3 Webhooks Saver
@app.route('/nomie3/data')
def nomie3Saver():
    success = True
    if success:
        return '{"success": "true"}'
    else:
        return '{"success": "false"}'

@app.route("/secure", methods=['POST'])
def parse_request():
    # Preparing for future developments
    return "None"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    app.run(host='0.0.0.0', port=port, debug=True)

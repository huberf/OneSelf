# Loads config file and returns global config
import json

def getConfig():
    try:
        configFile = open('config.json')
        configRaw = configFile.read()
        config = json.loads(configRaw)
        return config
    except:
        print('You need to create or edit config.json in the directory you are executing.')
        return None

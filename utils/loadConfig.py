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

def setConfig(config):
    try:
        configFile = open('config.json', 'w')
        configFile.write(json.dumps(config, indent=2))
        configFile.close()
    except:
        print('There was an error writing the config file.')

# This script is intended to intelligently monitor your nutrition data
import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils

config = loadConfig.getConfig()

genetic_data = {}

try:
    genome_file = open('records/genome_data.txt')
    raw_contents = genome_file.read()
except IOError as e:
    print('Make sure you\'ve setup your genetic data')
    sys.exit()

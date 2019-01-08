# Standard imports. Add analysis specific ones.
import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils
import generator

config = loadConfig.getConfig()

# Write your analysis script here

parts = [
        ['header', ['Boilerplate Report']],
        ]
generator.build_report('lastfm_main', parts)

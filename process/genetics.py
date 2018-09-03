# This script is intended to intelligently monitor your nutrition data
import sys
import datetime
import json
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import loadConfig
import utils

config = loadConfig.getConfig()

genetic_data = []
genetic_dictionary = {}

try:
    genome_file = open('records/genome_data.txt')
    raw_contents = genome_file.read()
    lines = raw_contents.split('\n')
    for i in lines:
        if len(i) > 0 and i[0] == '#':
            continue # Line is a comment
        elif len(i) > 0:
            # 0=rsid, 1=chromosome, 2=position, 3=genotype
            columns = i.split('\t')
            genetic_data += [{
                'rsid': columns[0],
                'chromosome': columns[1],
                'position': columns[2],
                'genotype': columns[3]
                }]
            genetic_dictionary[columns[0]] = {
                    'chromosome': columns[1],
                    'position': columns[2],
                    'genotype': columns[3]
                    }
except IOError as e:
    print('Make sure you\'ve setup your genetic data')
    sys.exit()

print('You have {0} genotypes sequenced.'.format(len(genetic_data)))

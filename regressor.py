import os
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

all_aggregates = os.listdir('aggregates/')
print('These are the files you can compare:')
for i,val in enumerate(all_aggregates):
    print('{0}: {1}'.format(i, val))
print()
while True:
    print('Select two files to regress by inputing their number from the list above.')
    select1 = int(input('Metric 1: '))
    select2 = int(input('Metric 2: '))

    file1 = all_aggregates[select1]
    file2 = all_aggregates[select2]

    conts1 = open('aggregates/' + file1).read()
    conts2 = open('aggregates/' + file2).read()

    map1 = {}
    map2 = {}

    for i in conts1.split('\n'):
        if len(i) > 0:
            metrics = i.split(',')
            map1[metrics[0]] = float(metrics[1])
    for i in conts2.split('\n'):
        if len(i) > 0:
            metrics = i.split(',')
            map2[metrics[0]] = float(metrics[1])

    x = []
    y = []

    IGNORE_ZEROS = True
    if IGNORE_ZEROS:
        # TODO: Add inference logic
        for i in map1.keys():
            if map1[i] == 0:
                continue
            try:
                val2 = map2[i]
                if val2 == 0:
                    continue
                x += [map1[i]]
                y += [val2]
            except:
                pass
    else:
        print('Mode not supported yet')

    # now do regression
    if len(x) > 0:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        print('Slope: {0}'.format(slope))
        print('Intercept: {0}'.format(intercept))
        print('R Value: {0}'.format(r_value))
    else:
        print('There was no data connected.')
    print()

    try:
        choice = raw_input('Show graphs? [Y/N]: ')
    except NameError:
        choice = input('Show graphs? [Y/N]: ')
    if len(choice) > 0 and (choice[0] == 'y' or choice[0] == 'Y'):
        plt.scatter(x, y)
        plt.ylabel(file2)
        plt.xlabel(file1)
        plt.show()

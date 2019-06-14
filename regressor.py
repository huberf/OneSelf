import os

all_aggregates = os.listdir('aggregates/')
print('These are the files you can compare:')
for i,val in enumerate(all_aggregates):
    print('{0}: {1}'.format(i, val))
print()
print('Select two files to regress by inputing their number from the list above.')
select1 = int(input('Metric 1: '))
select2 = int(input('Metric 2: '))

file1 = all_aggregates[select1]
file2 = all_aggregates[select2]

conts1 = open(file1).read()
conts2 = open(file2).read()

map1 = {}
map2 = {}

for i in conts1.split('\n')
    if len(i) > 0:
        metrics = i.split(',')
        map1[metrics[0]] = float(metrics[1])
for i in conts2.split('\n')
    if len(i) > 0:
        metrics = i.split(',')
        map2[metrics[0]] = float(metrics[1])

x = []
y = []

IGNORE_ZEROS = True
if IGNORE_ZEROS:
    # TODO: Add inference logic
    pass
else:
    print('Mode not supported yet')

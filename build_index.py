import os
import generator

files = os.listdir('html')

reports = []
for i in files:
    if i.endswith('.html') and not i == 'index.html':
        print(i)
        reports += [[i[:-5], i]]

generator.build_index(reports)

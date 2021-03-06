import json
import datetime
import os

parts = json.loads(open('generator/parts.json', 'r').read())

###########################
# Specific Helper Methods #
###########################
def build_top3(name, features, depth=False):
    parts = [name]
    for i in range(0,3):
        try:
            if depth:
                parts += [features[i][0]]
            else:
                parts += [features[i]]
        except:
            parts += ['None']
    return ['top3', parts]

def build_top3_count(name, features):
    parts = [name]
    for i in range(0,3):
        try:
            parts += [features[i][0], features[i][1]]
        except:
            parts += ['None', 'N/A']
    return ['top3_count', parts]


###########################
# General Methods         #
###########################
def build_index(report_list):
    ''' report_list is a list of the format [ ['Report Name', 'file_name'], ...]
    '''
    body = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="main.css">
  </head>
  <body>
    <div class="main-container">
      <h1>OneSelf Report List</h1>
      <ul>
      {0}
      </ul>
    </div>
  </body>
</html>'''
    list_html = ''
    for i in report_list:
        list_html += '<li><a href="{0}">{1}</a></li>'.format(i[1], i[0])
    contents = body.format(list_html)
    open('html/index.html', 'w').write(contents)

def build_report(name, contents):
    ''' name is a string used as the HTML file name
        contents is a list of format [ ['part_name', [val1, val2]], ...]
    '''
    body = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="main.css">
  </head>
  <body>
    <div class="main-container">
      {0}
    </div>
  </body>
</html>'''
    inside_contents = ""
    for item in contents:
        template = parts[item[0]]
        if not template['num_args'] == len(item[1]):
            print('Argument conflict')
            pass
        inside_contents += template['html'].format(*item[1])
        inside_contents += '<div class="divider"></div>'
    inside_contents += parts['paragraph']['html'].format('Last Updated: {0}'.format(datetime.datetime.now()))
    inside_contents += parts['link']['html'].format('index.html', 'Back to Report List')
    contents = body.format(inside_contents)
    file_name = 'html/{0}.html'.format(name)
    open(file_name, 'w').write(contents)

def check_figure_directory():
    check_html_directory('figures')

def check_html_directory(dir_path):
    directory = 'html/{0}'.format(dir_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

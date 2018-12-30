import json

parts = json.loads(open('generator/parts.json', 'r').read())

def build_index(report_list):
    ''' report_list is a list of the format [ ['Report Name', 'file_name'], ...]
    '''
    body = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
  </head>
  <body>
    <h1>OneSelf Report List</h1>
    {0}
  </body>
</html>'''
    list_html = ''
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
  </head>
  <body>
    {0}
  </body>
</html>'''
    inside_contents = ""
    for item in contents:
        template = parts[item[0]]
        if not template['num_args'] == len(item[1]):
            print('Argument conflict')
            pass
        inside_contents += template['html'].format(*item[1])
    contents = body.format(inside_contents)
    file_name = 'html/{0}.html'.format(name)
    open(file_name, 'w').write(contents)

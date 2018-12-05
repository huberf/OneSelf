import sys
from os import path
import datetime
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils
import utils.loadConfig

import csv

def load_data():
    data_file = utils.load_file('mint_transactions.csv')
    data_reader = csv.reader(data_file)
    transaction_data = []
    first_row = True
    for row in data_reader:
        if first_row:
            first_row = False
            continue
        transaction = {
            'date': row[0],
            'description': row[1],
            'og description': row[2],
            'amount': float(row[3]),
            'type': row[4],
            'category': row[5],
            'account': row[6],
            'labels': row[7],
            'notes': row[8]
            }
        if row[4] == 'debit':
            transaction['net'] = - float(row[3])
        else:
            transaction['net'] = float(row[3])
        transaction_data += [transaction]
    return { 'transactions': transaction_data }

def last_days_data(data, days):
    for i in data['transactions']:
        comp_date = i['date']
        day = comp_date.split('/')[1]
        month = comp_date.split('/')[0]
        year = comp_date.split('/')[2]
        comp_date = datetime.datetime(day=int(day), month=int(month), year=int(year))
        if utils.is_within_days(comp_date, days):
            yield i
    

# By count or value
def category_count(data, type='count'):
    buckets = {}
    for i in data['transactions']:
        try:
            if type == 'value':
                buckets[i['category']] = i['net']
            else:
                buckets[i['category']] += 1
        except:
            if type == 'value':
                buckets[i['category']] -= i['net']
            else:
                buckets[i['category']] = 1
    return buckets

# By count or value
def top_category(data, type='count'):
    buckets = category_count(data, type)
    max_count = -1
    max_categories = []
    for i in list(buckets.keys()):
        if buckets[i] > max_count:
            max_count = buckets[i]
            max_categories = [i]
        elif buckets[i] == max_count:
            max_categories += [i]
    return max_categories

if __name__ == '__main__':
    data = load_data()
    last_month = list(last_days_data(data, 30))
    last_month_data = { 'transactions': last_month }
    # Now show off what we can do
    print('Top category by count: ', top_category(data))
    print('Top category by value: ', top_category(data, 'value'))
    # Now show month level data
    print('Top Monthly category by count: ', top_category(last_month_data))
    print('Top Monthly category by value: ', top_category(last_month_data, 'value'))

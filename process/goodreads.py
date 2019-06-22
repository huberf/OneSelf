import sys
from os import path
import datetime
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils
import utils.loadConfig
import generator

import csv

def load_data():
    data_file = utils.load_file('goodreads_library_export.csv')
    data_reader = csv.reader(data_file)
    transaction_data = []
    first_row = True
    books = []
    for row in data_reader:
        if first_row:
            first_row = False
            continue
        # Row keys: Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Average Rating
        # Publisher,Binding,Number of Pages,Year Published,Original Publication Year,Date Read,Date Added,
        # Bookshelves,Bookshelves with positions,Exclusive Shelf,My Review,Spoiler,Private Notes,Read Count,
        # Recommended For,Recommended By,Owned Copies,Original Purchase Date,Original Purchase Location,
        # Condition,Condition Description,BCID
        keys = [
                'book_id', 'title', 'author', 'author l-f', 'additional_authors',
                'isbn', 'isbn13', 'my_rating', 'avg_rating', 'publisher',
                'binding', 'number_of_pages', 'publish_year', 'original_publish_year',
                'date_read', 'date_added', 'bookshelves', 'bookshelves_with_positions',
                'exclusive_shelf', 'my_review', 'spoiler', 'private_notes', 'read_count',
                'recommended_for', 'recommended_by', 'owned_copies', 'original_purchase_date',
                'original_purchase_location', 'condition', 'condition_description', 'bcid'
                ]
        book = { }
        for i,val in enumerate(keys):
            book[val] = row[i]
        books += [book]
    return { 'books': books }

def books_in_year(books, year):
    count = 0
    for i in books:
        if len(i['date_read']) > 4:
            book_year = i['date_read'][0:4]
            if book_year == year:
                count += 1
    return count

def books_in_past_year(books):
    year = str(datetime.datetime.now().year)
    return books_in_year(books, year)

def projected_reading(books):
    current_count = books_in_past_year(books)
    current = datetime.datetime.now()
    days = (datetime.date.today() - datetime.date(current.year, 1, 1)).days
    percent_through = float(days)/365
    if percent_through > 0:
        return current_count/percent_through
    else:
        return 0

def avg_page_count(books):
    count = 0
    pages = 0
    for i in books:
        try:
            pages += int(i['number_of_pages'])
        except ValueError: # Doesn't have a page count
            pass # Do nothing
        count += 1
    if count > 0:
        return float(pages) / count
    else:
        return 0

def top_authors(books):
    author_map = {}
    for i in books:
        try:
            author_map[i['author']] += 1
        except:
            author_map[i['author']] = 1
    sorted_list = sorted(author_map.items(), key=lambda kv: kv[1])
    sorted_list.reverse()
    return sorted_list

data = load_data()
book_count = len(data['books'])
print('Books Read: {0}'.format(book_count))
this_year_book_count = books_in_past_year(data['books'])
print('Books in Past Year: {0}'.format(this_year_book_count))
my_avg_page_count = avg_page_count(data['books'])
print('Avg Page Count: {0:.1f}'.format(my_avg_page_count))
my_projected_reading = projected_reading(data['books'])
print('Projected Year Count: {0:.0f}'.format(my_projected_reading))
author_list = top_authors(data['books'])

# Now generate HTML report
parts = [
        ['header', ['Goodreads Report']],
        ['big_num', ['Books Read', book_count]],
        ['big_num', ['Books in Past Year', this_year_book_count]],
        ['big_num', ['Average Page Count', my_avg_page_count]],
        ['big_num', ['Projected Year Count', my_projected_reading]],
        generator.build_top3_count('Top Authors', author_list)
        ]
generator.build_report('goodreads_main', parts)

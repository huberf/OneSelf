import sys
from os import path
import datetime
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import utils
import utils.loadConfig

import csv

def load_data():
    data_file = utils.load_file('goodreads_library_export.csv')
    data_reader = csv.reader(data_file)
    transaction_data = []
    first_row = True
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
        books = { }
        for i,val in enumerate(keys):
            books[val] = row[i]
    return { 'books': books }

data = load_data()
book_count = len(data['books'])
print('Books Read: {0}'.format(book_count))

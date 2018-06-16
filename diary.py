#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('diary.db')

class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def initialize():
    """Create the database and table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)

def clear():
    os.system('cls' if os.name =='nt' else 'clear')

def menu_loop():
    """Show the menu."""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            #when called on a function name
            #.__doc__ returns the doc string of that function 
            #the values in the menu Ordered Dict are function names 
            #therefore calling value.__doc__ will automatically generate 
            #the choice name for us in the print statement
            print('{}) {}'.format(key, value.__doc__)) 
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()

def add_entry():
    """Add an entry."""
    print("Enter your entry. Press ctrl+d when finished.")
    data = sys.stdin.read().strip()

    if data:
        if input('Save entry? [y/n]').lower() != 'n':
            Entry.create(content=data)
            print("Saved successfully!")

def view_entries(search_query=None):
    """View previous entries."""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print('='*len(timestamp))
        print(entry.content)
        print('\n\n'+'='*len(timestamp))
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)

def search_entries():
    """Search previous entries."""
    view_entries(input('Search query: '))

def delete_entry(entry):
    """Delete an entry."""
    if input("Are you sure? [yN]").lower() == 'y':
        entry.delete_instance()
        print("Entry deleted!")


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
    ])

if __name__ == '__main__':
    initialize()
    menu_loop()

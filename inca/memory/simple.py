"""
"""

from sqlitedict import SqliteDict
import warnings
import os

def here(x):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), x)

def remember(key, value):
    with SqliteDict(here('memory.db'), tablename="simple") as storage:
        if key in storage:
            warnings.warn("Key exists already; not saving")
            return
        else:
            storage[key] = value
            storage.commit()    

def dump():
    with SqliteDict(here('memory.db'), tablename="simple") as storage:
        for key,value in storage.items():
            print('key: \t{}'.format(key))
            print('value: \t{}'.format(value))

def retrieve(name):
    with SqliteDict(here('memory.db'), tablename="simple") as storage:
        if name not in storage:
            return "404. Not Found" 
        else:
            return storage[name]




    
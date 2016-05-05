"""
"""

from sqlitedict import SqliteDict
import warnings


def remember(key, value):
    with SqliteDict('memory.db', tablename="simple") as storage:
        if key in storage:
            warnings.warn("Key exists already; not saving")
            return
        else:
            storage[key] = value
            storage.commit()    

def dump():
    with SqliteDict('memory.db', tablename="simple") as storage:
        for key,value in storage.items():
            print('key: \t{}'.format(key))
            print('value: \t{}'.format(value))
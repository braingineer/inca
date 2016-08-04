from sqlitedict import SqliteDict
import warnings
import os
from functools import wraps, partial

this_db = 'taskstack.db'

def here(x):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), x)

def wraptext(s, pre='', post='\n', n=30):
    out = ""
    cap = ""
    for token in s.split(" "):
        cap += token + " "
        if len(cap) > n:
            out += pre + cap + post
            cap = ""
    if len(cap) > 0:
        out += pre + cap + post
    return out

def access(func=None, db_name='generic.db', tablename='default'):
    if func is None:
        return partial(access, db_name=db_name, tablename=tablename)
    @wraps(func)
    def new_func(*args, **kwargs):
        with SqliteDict(here(db_name), tablename=tablename) as storage:
            out = func(storage, *args, **kwargs)
            storage.commit()
        return out
    return new_func

@access(db_name='taskstack.db', tablename='tasks')
def add(storage, shortname, description, urgency, date):
    if shortname in storage:
        if isinstance(storage[shortname], int):
            next_idx = str(storage[shortname])
            storage[shortname] += 1
        else:
            storage[shortname+'0'] = storage[shortname]
            storage[shortname] = 1
            next_idx = str(1)
        shortname = shortname+next_idx
    storage[shortname] = {'description':description,
                          'urgency':urgency,
                          'date': date}     

@access(db_name='taskstack.db', tablename='tasks')
def list_contents(storage, verbose=True):
    keys = sorted(storage.keys())
    if len(keys) == 0:
        print("<empty>")
    for i, k in enumerate(keys):
        print("{}. {}".format(i, k))
        if verbose:
            for field in ("description", "urgency", "date"):
                print("\t{}: {}".format(field, wraptext(storage[k][field], post='\n\t\t', n=40)))

@access(db_name='taskstack.db', tablename='tasks')
def delete(storage, name):
    del storage[name]

@access(db_name='taskstack.db', tablename='tasks')
def interactive_delete(storage):
    try:
        input = raw_input
    except:
        pass
    deleting = True
    while deleting:
        list_contents()
        entry = input("Entry to delete (exit to exit)>  ")
        if entry == 'exit':
            deleting = False
            continue
        try:
            entry = int(entry)
            assert entry < len(storage.keys())
        except:
            print("Bad entry.")
            continue
        entry_name = sorted(storage.keys())[entry]
        delete(entry_name)
        print("{} has been deleted".format(entry_name))


@access(db_name='taskstack.db', tablename='tasks')
@access(db_name='taskstack.db', tablename='tracker')
def next_item(tracker, storage):
    if len(storage.keys()) == 0:
        return 'stack empty'


    if 'index' not in tracker:
        tracker['index'] = 0
    try:
        item_key = sorted(storage.keys())[tracker['index']]
    except IndexError:
        if len(storage) > 0:
            temp = dict(enumerate(storage.values()))
            storage.clear()
            storage.update(temp)
            storage.commit()
            tracker['index'] = 0
            item_key = sorted(storage.keys())[tracker['index']]


    tracker['index'] = (tracker['index'] + 1) % len(storage.keys())
    shortened_desc = " ".join(storage[item_key]['description'].split(" ")[:10]) + "..."
    urgency = storage[item_key]['urgency']
    urgency_msg = "status: "+ ("SUPER URGENT" if urgency >= 9 else 
                               ("Very Urgent" if urgency >= 7 else 
                                ("Fairly Urgent" if urgency >=5 else
                                 ("not very urgent"))))

    return item_key + " > " + urgency_msg + " > " + shortened_desc



    
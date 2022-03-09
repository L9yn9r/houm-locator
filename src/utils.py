from datetime import datetime, timedelta
import json, pickle



def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def get_mins(h):

    delta = timedelta(hours=int(h.split(':')[0]), minutes=int(h.split(':')[1]), seconds=int(h.split(':')[2]))
    minutes = delta.total_seconds()/60
    return(minutes)

def format_secs_to_time(secs):
     return str(timedelta(seconds= secs))

def format_mins_to_time(mins):
     return str(timedelta(minutes=mins))



def key_to_json(data):
    if data is None or isinstance(data, (bool, int, str)):
        return data
    if isinstance(data, (tuple, frozenset)):
        return str(data)
    raise TypeError

def to_json(data):
    if data is None or isinstance(data, (bool, int, tuple, range, str, list)):
        return data
    if isinstance(data, (set, frozenset)):
        return sorted(data)
    if isinstance(data, dict):
        return {key_to_json(key): to_json(data[key]) for key in data}
    raise TypeError

# data = {('category1', 'category2'): {frozenset(['cat1', 'cat2']): 1212}}
# json.dumps(to_json(data))

def convert_tojson(data):
#data = {('category1', 'category2'): 4}
    s = pickle.dumps(data) # serialized data
    d = pickle.loads(s) # the original dictionary
    return d
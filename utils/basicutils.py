import json, os.path
from functools import partial
    
def avg(lst):
    return sum(lst)/len(lst) if lst else ''
    
def bulk_search(search, lst, *args, **kwargs):
    """Applies search to every item in lst keeping all *args and **kwargs"""
    results = []
    for item in lst:
        results.extend(search(item, *args, **kwargs))
    return results

def import_json(path):
    """Returns dict from json file located at path if path exists. Returns an empty dict if otherwise."""
    if os.path.exists(path):
        try:
            with open(path) as jsonfile:
                local_dict = json.loads(next(jsonfile))
            print('Data loaded from {}.'.format(path))
        except StopIteration:
            clear_json(path)
            return import_json(path)
    else:
        local_dict = {}
        print('No file found at {}.'.format(path))
    return local_dict

def json_dump(path, local_dict):
    """Dumps local_dict into json file at path."""
    with open(path,'w') as output:
        json.dump(local_dict, output)
    print('Data dumped at {}.'.format(path))

def clear_json(path):
    """Clears json file located at path."""
    if os.path.exists(path):
        os.remove(path)
        print('Data at {} cleared.'.format(path))
    else:
        print('No file found at {}.'.format(path))

def dict_req(key, dictionary):
    """Attempts to return dictionary[key], returns None if key not found."""
    try:
        print(key, dictionary[key])
        return dictionary[key]
    except KeyError:
        return None
    
class memo(object):
    """Decorator to memoize functions, with memoized results stored in local_cache."""
    def __init__(self, func):
        self.func = func
        self.cache_path = 'utils/data/json/cache/{}.json'.format(func.__name__)
        self.local_cache = import_json(self.cache_path)
        
        
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return partial(self, obj)
    
    def __call__(self, *args, **kw):
        if 'cache' in kw.keys():
            if kw['cache'] == 'dump':
                json_dump(self.cache_path, self.local_cache)
                self.local_cache = import_json(self.cache_path)
            elif kw['cache'] == 'clear':
                clear_json(self.cache_path)
                self.local_cache = {}
        else:
            obj = args[0]
            key = self.func.__name__+ str(args[1:])+ str(kw.items())
            try:
                res = self.local_cache[key]
            except KeyError:
                res = self.local_cache[key] = self.func(*args, **kw)
            return res

class Tree:
    def __init__(self, tag, branches):
        assert len(branches) >= 1
        for b in branches:
            assert isinstance(b, (Tree, Leaf))
        self.tag = tag
        self.branches = branches 

class Leaf:
    def __init__(self,tag,word):
        self.tag = tag
        self.word = word
    


       
                            
                
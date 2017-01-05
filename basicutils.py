import json, os.path
from functools import partial

local_cache = {}
    
def bulk_search(search, lst, *args, **kwargs):
    results = []
    for item in lst:
        results.extend(search(item, *args, **kwargs))
    return results

def import_cache(path):
    global local_cache
    if os.path.exists(path):
        with open(path) as jsonfile:
            local_cache = json.loads(next(jsonfile))
            for key in local_cache:
                if isinstance(local_cache[key],list):
                    local_cache[key] = list(map(tuple, local_cache[key]))         


    
class memo(object):
    def __init__(self, func):
        self.func = func
        
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return partial(self, obj)
    
    def __call__(self, *args, **kw):
        global local_cache
        obj = args[0]
        key = self.func.__name__+ str(args[1:])+ str(kw.items())
        try:
            res = local_cache[key]
        except KeyError:
            res = local_cache[key] = self.func(*args, **kw)
        return res

def json_dump(path):
    global local_cache
    with open(path,'w') as output:
        json.dump(local_cache, output)
        local_cache = {}

def clear_cache(path):
    global local_cache
    if os.path.exists(path):
        os.remove(path)
    local_cache = {}
       
                            
                
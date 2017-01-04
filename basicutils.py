import json, os.path
from functools import partial


    
def bulk_search(search, lst, *args, **kwargs):
    results = []
    for item in lst:
        results.append(search(item, *args, **kwargs))
    return results

if os.path.exists('data/cached_searches.json'):
    with open('data/cached_searches.json') as jsonfile:
        local_cache = json.loads(next(jsonfile))
else:
    local_cache = {}
    
class memo(object):
    def __init__(self, func):
        self.func = func
        
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return partial(self, obj)
    
    def __call__(self, *args, **kw):
        obj = args[0]
        key = self.func.__name__+ str(args[1:])+ str(kw.items())
        try:
            res = local_cache[key]
        except KeyError:
            res = local_cache[key] = self.func(*args, **kw)
        return res

def json_dump():
    with open('data/cached_searches.json','w') as output:
        json.dump(local_cache, output)
       
                            
                
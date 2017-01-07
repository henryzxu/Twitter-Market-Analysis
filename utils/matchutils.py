import re
from utils import basicutils

def lev_dist(s1, s2):
    """Calculates Levenshtein distance between s1 and s2."""
    if len(s1) < len(s2):
        return lev_dist(s2,s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j+1] + 1
            deletions = current_row[j] + 1
            subs = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, subs))
        previous_row = current_row
    
    return previous_row[-1]

def fuzzy_search(s, lst, num_results = 5):
    """Returns the closest string in lst to s. 
    First returned list is a guaranteed match, 
    second returned list is acronyms and whole word matches, 
    third returned list uses the Levenshtein approach."""
    assert s and lst, 'Fuzzy search lists cannot be empty.'
    search_s = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', s.strip()))
    t1res, t2res, lev_search = [], [], []
    for string in lst:
        search_string = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', string.strip()))
        if search_string == search_s:
            return [string]
        matcht1 = re.search(r'\b' + r'\b[\w\s]*\b'.join(search_s.lower().split()) + r'\b',search_string.lower())
        if matcht1:
            t1res.append(string)
            t2res.append(string)
        else:
            matcht2 = search_s == search_s.upper() and re.search(r'[\s\w]*\b[a-z\s]*'.join(list(search_s)) + r'\w*\b.*', search_string) or matcht1
            if matcht2:
                t2res.append(string)
            else:
                match = re.search(r'.*' + r'\S*'.join(list(search_s)) + r'.*', search_string)
                if match:
                    lev_search += [string]
    return [t1res if len(t1res) == 1 else [], sorted(t2res[:num_results], key = len), sorted(lev_search, key = lambda s2: lev_dist(s, s2))[:10]] 
        
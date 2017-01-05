import re

def lev_dist(s1, s2):
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

def fuzzy_search(s, lst):
    search_s = s.strip().replace(',','')
    res, lev_search = [], []
    for string in lst:
        search_string = string.replace(',','')
        if search_string == search_s:
            return [string]
        match = re.search(r'\b' + search_s.lower() + r'\b',search_string.lower()) or search_s == search_s.upper() and re.search(r'\w*\b[a-z\s]*'.join(list(search_s)) + r'\w*\b.*', search_string)
        if match:
            res.append(string)
        else:
            match = re.search(r'.*' + r'\S*'.join(list(search_s)) + r'.*', string)
            if match:
                lev_search += [match.group()]
    return sorted(lev_search, key = lambda s2: lev_dist(s, s2))[:10] if not res else res 
        
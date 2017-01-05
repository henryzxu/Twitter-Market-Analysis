import re, matchutils

conjunctions = ['and']

def basic_ner(sentence):
    res, previous_word = [], None
    sentence = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', sentence)).strip().split(' ')
    for word in sentence:
        if word[0] == word[0].upper():
            res.append(word)
            previous_word = word
        elif word in conjunctions:
            if previous_word:
                previous_word = res[-1] = res[-1] + ' ' + word        
        else:
            previous_word = None
    return list_powerset(res)

def list_powerset(lst):
    result = [[]]
    for x in lst:
        result.extend([subset + [x] for subset in result])
    result.pop(0)
    return result


def fuzzy_ner(sentence, lst):
    found = []
    def finder(sublist, limit):
        nonlocal found
        if sublist:
            mod_sublist = []
            for company in sublist:
                matches = matchutils.fuzzy_search(' '.join(company), lst)
                if len(matches) < limit and len(matches) > 0:
                    found.extend(matches[:2])
                    sublist = [entry for entry in sublist if entry not in mod_sublist]
                    return finder([entry for entry in sublist if entry not in mod_sublist and 
                                   not any([x for x in entry if x[0] in ' '.join(matches)])], limit)
                elif len(matches) == 0:
                    mod_sublist.append(company)
            if limit == 2:
                finder(sublist, 5)
    finder(basic_ner(sentence), 2)
    return found
            
            
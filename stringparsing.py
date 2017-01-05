import re, matchutils

conjunctions = ['and']

def basic_ner(sentence):
    res, previous_word = [], None
    sentence = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', sentence)).strip().split(' ')
    for word in sentence:
        if word.isalpha() and word[0] == word[0].upper():
            res.append(word)
            previous_word = word     
        else:
            previous_word = None
    print(res)
    return list_powerset(res)

def list_powerset(lst):
    result = [[]]
    for x in lst:
        result.extend([subset + [x] for subset in result])
    result.pop(0)
    return result


def fuzzy_ner(sentence, lst):
    found = []
    def finder(sublist, tier):
        nonlocal found
        if sublist:
            for company in sublist:
                matches = matchutils.fuzzy_search(' '.join(company), lst)
                res = matches[tier]
                if res:
                    found.extend(res)
                    return finder([entry for entry in sublist if not any([x for x in entry if x[0] in ' '.join(res)])], tier)
            if tier == 0:
                finder(sublist, 1)
    finder(basic_ner(sentence), 0)
    return found
            
            
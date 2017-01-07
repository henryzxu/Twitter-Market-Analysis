import re, matchutils, basicutils, ner_lists
try:
    from nltk.tag import pos_tag
    from nltk import bigrams
    nltk_enabled = True
except ImportError:
    print('NLTK integration not available.')
    nltk_enabled = False
    
def basic_ner(sentence, power = True, locations = False):
    """Basic name entity recognizer. Searches for capitalized words, ignoring names listed in ner_lists"""
    res, previous_word = [], None
    mod_sentence = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', sentence)).strip().split(' ')
    for word in mod_sentence:
        if word.isalpha() and word[0] == word[0].upper() and (locations or word not in ner_lists.all_location_names):
            res.append(word)
            previous_word = word     
        else:
            previous_word = None
    if nltk_enabled:
        tagged_sentence = pos_tag(mod_sentence)
        for word, tag in tagged_sentence:
            if word in res and 'N' not in tag:
                res.remove(word)
    return list_powerset(res) if power else res

def list_powerset(lst):
    """Returns all subsets of lst."""
    result = [[]]
    for x in lst:
        result.extend([subset + [x] for subset in result])
    result.pop(0)
    return result


def fuzzy_parse(sentence, lst):
    """Returns the words in sentence with fuzzy matches to items in lst."""
    found = []
    def finder(sublist, tier):
        nonlocal found
        if sublist:
            for company in sublist:
                matches = matchutils.fuzzy_search(' '.join(company), lst)
                res = matches[tier]
                if res:
                    found.append([' '.join(company), res])
                    return finder([entry for entry in sublist if not any([x for x in entry if x[0] in ' '.join(res)])], tier)
            if tier == 0:
                finder(sublist, 1)
    finder(basic_ner(sentence), 0)
    return found

def connotation_dump(path, sentence, value):
    """Associates all words, excluding parsed proper nouns, in sentence with value. 
    Each association is stored in a json file dumped at path."""
    try:
        word_connotations = basicutils.import_json(path)
        sentence = re.sub(r'[^\w\s]','', sentence)
        proper_nouns = basic_ner(sentence, power = False, locations = True)
        split_sent = sentence.split()
        for word in split_sent:
            if word in proper_nouns:
                pass
            else:            
                word = word.lower()
                try:
                    word_connotations[word].append(value)
                except KeyError:
                    word_connotations[word] = [value]
        if nltk_enabled:
            for bigram_tuple in bigrams(split_sent):
                if any([word for word in bigram_tuple 
                        for p_noun in proper_nouns 
                        if word == p_noun]):
                    pass
                else:
                    bigram_tuple = ' '.join([word.lower() 
                                             for word in bigram_tuple])
                    try:
                        word_connotations[bigram_tuple].append(value)
                    except KeyError:
                        word_connotations[bigram_tuple] = [value]
        basicutils.json_dump(path, word_connotations)
    except:
        print('Failed to dump data at {}'.format(path))

def list_bigrams(sentence_list):
    """Uses NLTK's bigram function to return the bigrams of sentence_list."""
    assert nltk_enabled
    return bigrams(sentence_list)
            
## Twitter Market Analysis

A research project to predict market movement based on short strings such as news headlines and Twitter tweets using language parsing, database lookup, JSON storage, and fuzzy searching. 

All results are dependant on the size of training data set.

### Introduction

In an era where the news is dictated not by veracity, but by speed, the ability to parse headlines as they come is crucial to maintaining the upper edge in market operations. While true natural language processing has yet to achieved, this repository gives one approach to analyzing sentence connotations. By training the computer to associate each word with a particular market movement, it can give a general gauge of how the market will react to a particular piece of information. 

### Features

#### Company Parsing
```markdown
In[1]: w = StockData()
       w.news_impact(datetime.datetime(2017,1,5),"Macy's to cut more than 10,000 jobs, close 68 stores")
```

```markdown
Company: Macy's Inc	Previous Day Close: 35.84	Next Day Open: 30.82	Net Change: -14.006696428571436
No file found at data/word_connotations.json.
Data dumped at data/word_connotations.json.

Out[1]: ["Negative for Macy's Inc"]
```

#### Market Prediction
```markdown
In[2]: w.impact_prediction('Sears facing dismal holiday retail season.')
```

```markdown
Data loaded from data/word_connotations.json.
holiday retail [-14.006696428571436]
retail season [-14.006696428571436]
facing [-14.006696428571436]
dismal [-14.006696428571436]

Out[2]: [(-14.006696428571436, 'Sears Canada Inc. '), (-14.006696428571436, 'Sears Holdings Corporation'), (-14.006696428571436, 'Sears Hometown and Outlet Stores, Inc.')]
```

#### Database Lookup
```markdown
In[3]: w.lookup(search_info = ['symbol', 'name', 'ipoyear', 'marketcap'], name = 'Mgmt')[:2]
```

```markdown
Out[3]: [('ARES', 'Ares Management L.P.', '2014', '$3.78B'), ('WM', 'Waste Management, Inc.', 'n/a', '$31.39B')]
```

```markdown
In[4]: w.lookup(ipoyear = list(range(1998,2000)), se = 'amex')[:2]
```

```markdown
In[5]: [('AMKR', 'Amkor Technology, Inc.', 'nasdaq'), ('AXTI', 'AXT Inc', 'nasdaq')]
```

### Additional Features
* CSV to SQLite3 conversion with primary key specification
* Memoization of all database queries and historical stock prices
* 3-tier fuzzy search:
    1. Guaranteed matches
    2. Acronyms and whole word matches
    3. Supplied list ranked by Levenshtein distance

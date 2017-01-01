# -*- coding: utf-8 -*-

import urllib.request, csv, re, sqlite3

def company_table(se = 'nasdaq', sql = False):
    """Returns table of company data from stock exchange 'se' 
    where each row contains the ticker symbol, lowercase company name, and NASDAQ website"""
    assert se in ['nasdaq','nyse'], 'Not a valid stock exchange'
    try:
        with urllib.request.urlopen('http://www.nasdaq.com/screening/company-list.aspx') as response:
            html = response.read()
        html = str(html)
        search_url = r'href=.(\S+' + se + r'\S+download)'
        ticker_file_url = re.search(search_url,html)
        if ticker_file_url:
            url = ticker_file_url.group(1)
        else:
            print(search_url)
        with urllib.request.urlopen(url) as response:
            tickers = csv.reader(response.read().decode('utf-8').splitlines())
    except:
        with open('data/companylist' + se + '.csv', newline = '') as csvfile:
            tickers = csv.reader(csvfile)
            
    tickertable = []
    for row in tickers:           
        tickertable.append(row)

    if sql:
        conn = sqlite3.connect('data/companysql.sql')
        curs = conn.cursor()
        curs.executescript("DROP TABLE IF EXISTS companysql; CREATE TABLE companysql (symbol, name, sector);")
        for row in tickertable:
            to_db = [str(row[x]) for x in [0,1,6]]
            curs.execute("INSERT INTO companysql (symbol, name, sector) VALUES (?, ?, ?);", to_db)
            conn.commit()
        conn.close()
        
    return tickertable[1:]

    
    
        



# -*- coding: utf-8 -*-

import urllib.request, csv, re, sqlite3
import os.path

def company_table(se = 'nasdaq', update = False):
    """Returns table of company data from stock exchange 'se' 
    where each row contains the ticker symbol, lowercase company name, and NASDAQ website"""
    se = se.lower()
    assert se in ['nasdaq','nyse', 'amex'], 'Not a valid stock exchange'
    if not update:
        if os.path.exists('data/companylist' + se + '.csv'):
            with open('data/companylist' + se + '.csv', newline = '') as csvfile:
                tickers = csv.reader(csvfile)
                tickertable = csv_to_table(tickers, se)
            return tickertable[1:]
        else:
            return company_table(se = se, update = True)
    else:
        try: 
            with urllib.request.urlopen('http://www.nasdaq.com/screening/company-list.aspx') as response:
                html = response.read()
            html = str(html)
            search_url = r'href=.(\S+' + se + r'\S+download)'
            ticker_file_url = re.search(search_url,html)
            if ticker_file_url:
                url = ticker_file_url.group(1)
            else:
                raise Exception
            urllib.request.urlretrieve(url, 'data/companylist' + se + '.csv') 
        except:
            print('Failed to update ' + se.upper() + ' exchange table')
        tickertable = company_table(se = se)
        data_to_sql(tickertable, se)
        return tickertable

def csv_to_table(csv, se):
    table = []
    for row in csv:
        table.append(row)
    return table

def data_to_sql(table, se):
    conn = sqlite3.connect('data/companysql' + se + '.sql')
    curs = conn.cursor()
    curs.executescript("DROP TABLE IF EXISTS companytable; CREATE TABLE companytable (symbol, name, sector);")
    for row in table:
        to_db = [str(row[x]) for x in [0,1,6]]
        curs.execute("INSERT INTO companytable (symbol, name, sector) VALUES (?, ?, ?);", to_db)
        conn.commit()
    conn.close()
    
        



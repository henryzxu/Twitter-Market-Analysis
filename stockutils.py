# -*- coding: utf-8 -*-

import urllib.request, csv, re, sqlite3, html, os.path

se_list = ['nasdaq','nyse', 'amex']
def company_table(se = None, update = False, force_update = False):
    """Returns table of company data from stock exchange 'se' 
    where each row contains the ticker symbol, lowercase company name, and NASDAQ website"""
    assert se is None or se in se_list, 'Not a valid stock exchange'
    if not se:
        tickertable = []
        for se in se_list:
            tickertable.extend(company_table(se, update))
        data_to_consolidated_sql(tickertable, 'companytable', 'data/completecompanylist.sql')
        return tickertable
    se = se.lower()
    if not update and not force_update:
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
        if not force_update:
            data_to_consolidated_sql(tickertable, 'companytable', 'data/companysql' + se + '.sql')
        else:
            data_to_sql(tickertable,se)
        return tickertable

def csv_to_table(csv, se):
    table = []
    for row in csv:
        row.append(se)
        table.append(row)
    return table

def data_to_sql(table, se):
    """Creates a SQL table using data from parameter table. Not in use."""
    conn = sqlite3.connect('data/companysql' + se + '.sql')
    curs = conn.cursor()
    curs.executescript("DROP TABLE IF EXISTS companytable; CREATE TABLE companytable (symbol, name, sector, se);")
    for row in table:
        to_db = [html.unescape(str(row[x])) for x in [0,1,6,9]]
        curs.execute("INSERT INTO companytable (symbol, name, sector, se) VALUES (?, ?, ?, ?);", to_db)
    conn.commit()
    conn.close()
    
def data_to_consolidated_sql(table, dest_table, dest_name):
    """Merges data from table into dest_table at dest_name."""
    conn = sqlite3.connect(dest_name)
    curs = conn.cursor()
    curs.executescript("CREATE TABLE IF NOT EXISTS " + dest_table + "(symbol PRIMARY KEY, name, sector, se);")
    for row in table:
        to_db = [html.unescape(str(row[x])) for x in [0,1,6,9]]
        curs.execute("INSERT OR IGNORE INTO " + dest_table + "(symbol, name, sector, se) VALUES (?, ?, ?, ?);", to_db)
    conn.commit()
    conn.close()
    
    
        



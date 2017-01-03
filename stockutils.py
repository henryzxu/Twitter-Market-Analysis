# -*- coding: utf-8 -*-

import urllib.request, csv, re, sqlite3, html, os.path

se_list = ['nasdaq','nyse', 'amex']
sql_path = 'data/completecompanylist.sql'
sql_table_name = 'companytable'
def company_table(se = None, update = False, update_sql = False):
    """Returns table of company data from stock exchange 'se' 
    where each row contains the ticker symbol, lowercase company name, and NASDAQ website"""
    assert se is None or se in se_list, 'Not a valid stock exchange'
    if not se:
        tickertable = {}
        for se in se_list:
            tickertable = {**tickertable,**company_table(se, update)}
        return tickertable
    se = se.lower()
    if not update:
        if update_sql:
            if os.path.exists('data/companylist' + se + '.csv'):
                with open('data/companylist' + se + '.csv', newline = '') as csvfile:
                    dict_to_sql(csvfile, se, sql_table_name, sql_path)
            else:
                return company_table(se = se, update = True)
        tickertable = sql_to_dict(sql_path, sql_table_name)     
        return tickertable
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
        tickertable = company_table(se = se, update_sql = True)
        return tickertable

def csv_to_table(csvfile, se):
    tickers = csv.DictReader(csvfile)
    table = {}
    for row in tickers:
        table[html.unescape(str(row['Name']))] = html.unescape(str(row['Symbol']))
    return table


def dict_to_sql(csvfile, se, dest_table, dest_name):
    """Merges data from csvfile into dest_table at dest_name."""
    full_data = csv.DictReader(csvfile)
    first_row = next(full_data)
    order_keys = [item for item in first_row.keys() if item != '' and item.lower() != 'name'] + ['Name']
    column_names = [item.lower().replace(' ','') for item in order_keys[:-1] if item != '']
    column_names += ['name PRIMARY KEY']
    conn = sqlite3.connect(dest_name)
    curs = conn.cursor()
    curs.executescript("CREATE TABLE IF NOT EXISTS " + dest_table + "(" + ','.join(column_names + ['se']) + ");")
    column_names.pop()
    column_names.append('name')
    for row in full_data:
        to_db = [html.unescape(str(row[x])) for x in order_keys]
        curs.execute("INSERT OR IGNORE INTO " + dest_table + " (" + ','.join(column_names + ['se']) + ") VALUES  (" + ','.join(['?']*(len(order_keys)+1))+ ");", to_db + [se])
    conn.commit()
    conn.close()
    return

def sql_to_dict(sql_loc, table_name):
    """Returns dictionary where keys are company names and 
    values are their respective ticker symbols."""
    return_dict = {}
    conn = sqlite3.connect(sql_loc)
    curs = conn.cursor()
    entries = curs.execute("SELECT name,symbol from " + table_name + ";").fetchall()
    for name,symbol in entries:
        return_dict[name] = symbol
    return return_dict


#Miscellaneous Functions 

#Replaced by dict_to_sql
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
    return
    
#Fuzzy matching moved to matchutils.py
def closest_match(lst, string, upper = False):
    """Matches closest string in lst to string."""
    assert lst, 'List parameter cannot be empty'
    results = []
    for potential in lst:
        potential_name = potential[1]
        match = re.search(r'.*' + string + r'.*', potential_name)
        if match:  #if match of whole word
            results.append(potential)
        elif upper: #if acronym
            query = '.*'.join(list(potential_name))+r'.*'
            match = re.search(query, potential_name)
            if match:
                results.append(potential)
            return results if results else lst
    else:
        return results if results else closest_match(lst,string.upper(),upper = True)

        
            
    
    
        



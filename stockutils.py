# -*- coding: utf-8 -*-

import urllib.request, csv, re, sqlite3, html, os.path, config, collections

se_list = ['nasdaq','nyse', 'amex']
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
                    dict_to_sql(csvfile, se, config.sql_table_name, config.sql_path, 'Name')
            else:
                return company_table(se = se, update = True)
        tickertable = sql_to_dict(config.sql_path, config.sql_table_name)     
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

def dict_to_sql(csvfile, se, dest_table, dest_name, primary_key):
    """Merges data from csvfile into dest_table at dest_name."""
    full_data = csv.DictReader(csvfile)
    first_row = next(full_data)
    assert primary_key in first_row.keys(), 'Not a valid key.'
    order_keys = [item for item in first_row.keys() if item != '']
    primary_insert = primary_key.lower().replace(' ','')
    column_names = [item.lower().replace(' ','') if item != primary_key else primary_insert + ' PRIMARY KEY' for 
                    item in order_keys if item != ''] + ['se']
    conn = sqlite3.connect(dest_name)
    curs = conn.cursor()
    curs.executescript("CREATE TABLE IF NOT EXISTS " + dest_table + "(" + ','.join(column_names) + ");")
    column_names = [item.replace(primary_insert + ' PRIMARY KEY', primary_insert) for item in column_names]
    for row in full_data:
        to_db = [html.unescape(str(row[x])) for x in order_keys] + [se]
        curs.execute("INSERT OR IGNORE INTO " + dest_table + " (" + ','.join(column_names) + ") VALUES  (" + ','.join(['?']*(len(order_keys)+1))+ ");", to_db)
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
        return_dict[name] = name
    conn.close()
    return return_dict


def sql_search(path, table_name, search_terms, **conditions):
    """Searches the table_name at path for search_terms which fulfill conditions."""
    rows = []
    try:
        columns = []
        for column_name, param in conditions.items():
            assert param
            if not isinstance(param, list):
                if isinstance(param, str) or isinstance(param, int):
                    param = [param]
                elif isinstance(param, collections.Iterable):
                    param = list(param)
            conditional = ' AND ' if param[0] == '^' else ' OR '
            columns += [(' = ?' + conditional).join([column_name for _ in range(len(param))]) + ' = ?']  
        query = tuple([str(s) for s in flatten([param for param in conditions.values()])],)  
        conn = sqlite3.connect(path)
        c = conn.cursor()
        rows = c.execute('SELECT ' + ','.join(search_terms) + ' FROM ' + table_name + ' WHERE ' + ' AND '.join(columns) + ';', query).fetchall()
        conn.close()
    except (sqlite3.OperationalError, AssertionError) as e:
        pass
    return rows

def flatten(x):
    if isinstance(x, list):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]

#Deprecated Functions 

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

#Replaced by sql_to_dict
def csv_to_table(csvfile, se):
    """Converts csvfile into a dictionary where the keys are company names and the values are their respective symbols.'"""
    tickers = csv.DictReader(csvfile)
    table = {}
    for row in tickers:
        table[html.unescape(str(row['Name']))] = html.unescape(str(row['Symbol']))
    return table
    
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

        
            
    
    
        



import stockutils
import pandas_datareader.data as web, re, sqlite3, datetime

class StockData:
    def __init__(self, se = None, update = False, force_update = False):
        self.company_table = stockutils.company_table(se = se, update = update, force_update = force_update)
        self.se = se
   
    def lookup_ticker(self, company_name, sql = True):
        """Converts company_name to ticker symbol. Returns a tuple of (symbol, company name) 
        or returns an empty table if company or ticker is not found."""
        if isinstance(company_name,str):
            company_name = [company_name]
        result_table, conn = [], None 
        if not sql:
            for name in company_name:
                name = r'.*\s*'+name.lower()+r'.*'
                for row in self.company_table:
                    match = re.search(name,row[1].lower()) 
                    if match:
                        result_table.append((row[0],row[1],row[9]))
        elif self.se:
            conn = sqlite3.connect('data/companysql' + self.se + '.sql')
        else:
            conn = sqlite3.connect('data/completecompanylist.sql')
        if conn: 
            c = conn.cursor()
            for name in company_name:
                query = ('%'+name+'%',)
                rows = c.execute('SELECT symbol,name,se FROM companytable WHERE name LIKE ?;', query).fetchall()
                if rows:
                    for row in rows:
                        result_table.append(row)
                else:
                    print('Switching to table for ' + name + ' lookup.')
                    result_table.append(self.lookup_ticker(name, sql = False))
            conn.close()
        if result_table:
            return result_table.pop() if len(result_table) == 1 else result_table
        else:
            return ('N/A', company_name[0])
    
       #def stock_price(self, ticker, date):
        
            
        
        
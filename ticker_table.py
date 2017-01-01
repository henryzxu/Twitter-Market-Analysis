import urllib.request, csv, re

def company_table(se):
    """Returns table of company data from stock exchange 'se' 
    where each row contains the ticker symbol, lowercase company name, and NASDAQ website"""
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
        with open('data/companylist.csv', newline = '') as csvfile:
            tickers = csv.reader(csvfile)
    tickertable = []
    for row in tickers:           
            tickertable.append(row)
    return tickertable[1:]
        

        



#class that initializes and stores the EDGAR company data into a hash map (dictionary)
import requests
class EdgarData:
    
    def __init__(self, fileurl):
        self.fileurl = fileurl #url containing data
        self.company_name = {}
        self.stock_ticker = {}
        
        headers = {'User-Agent': 'MLT JC jonathancstr389@gmail.com' }
        r = requests.get(self.fileurl, headers=headers)
        
        if r.status_code == 200: #if fethcing data was succesful
            reqjson = r.json()
            for k, v in reqjson.items():
                if 'cik_str' in v and 'ticker' in v and 'title' in v:
                    cik = v['cik_str']
                    ticker = v['ticker']
                    title = v['title'] #company name
                    
                    if cik and ticker and title:
                        self.company_name[title] = (cik, ticker)
                        self.stock_ticker[ticker] = (cik, title)
                        
    #The The return values should be a tuple that at least includes CIK, Name, Ticker but could include more information.
    def name_to_cik(self, title):
        if title in self.company_name:
            cik, ticker = self.company_name[title]
            return cik, ticker, title
        
        
    def ticker_to_cik(self, ticker):
        if ticker in self.stock_ticker:
            cik, title = self.stock_ticker[ticker]
            return cik, ticker, title
        
        
s = EdgarData('https://www.sec.gov/files/company_tickers.json')
print(s.ticker_to_cik("TSLA"))
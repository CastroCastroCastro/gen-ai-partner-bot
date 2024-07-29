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
                    
                    #populate dictionaries with the company data
                    if cik and ticker and title:
                        self.company_name[title] = (cik, ticker)
                        self.stock_ticker[ticker] = (cik, title)
                        
    #gets CIK information by company name
    def name_to_cik(self, title):
        if title in self.company_name:
            cik, ticker = self.company_name[title]
            return cik, ticker, title
        
    #gets CIK information by stock ticker
    def ticker_to_cik(self, ticker):
        if ticker in self.stock_ticker:
            cik, title = self.stock_ticker[ticker]
            return cik, ticker, title
        
    #private method to fetch filing data for a given CIK
    def _fetch_cik_data(self, cik):
        url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
        headers = {'User-Agent': 'MLT JC jonathancstr389@gmail.com'}
        r = requests.get(url, headers=headers)
        
        if r.status_code == 200:
            return r.json() #return the JSON data if successful
        else:
            print(f"Error fetching CIK data: {r.status_code}")
            return None
        
    #private method to fetch the content of a specific document
    def _get_document_content(self, cik, accession_number, primary_document):
        url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{primary_document}"
        headers = {'User-Agent': 'MLT JC jonathancstr389@gmail.com'}
        r = requests.get(url, headers=headers)
        
        if r.status_code == 200:
            return r.content #returns the content of the document
        else:
            return f"Error fetching document content: {r.status_code}"
        
    #method to get the content of the 10-K annual filing for a given CIK and year
    def annual_filing(self, cik, year):
        data = self._fetch_cik_data(cik)
        if data:
            filings = data.get('filings', {}).get('recent', {})
            for i in range(len(filings.get('form', []))):
                if filings['form'][i] == '10-K' and str(year) in filings['filingDate'][i]:
                    accession_number = filings['accessionNumber'][i].replace('-', '')
                    primary_document = filings['primaryDocument'][i]
                    return self._get_document_content(cik, accession_number, primary_document)
        return "10-K filing not found for the specified year."
    
    #method to get the content of the 10-Q quarterly filing for a given CIK, year, and quarter
    def quarterly_filing(self, cik, year, quarter):
        data = self._fetch_cik_data(cik)
        if data:
            filings = data.get('filings', {}).get('recent', {})
            for i in range(len(filings.get('form', []))):
                if filings['form'][i] == '10-Q' and str(year) in filings['filingDate'][i]:
                    accession_number = filings['accessionNumber'][i].replace('-', '')
                    primary_document = filings['primaryDocument'][i]
                    return self._get_document_content(cik, accession_number, primary_document)
        return "10-Q filing not found for the specified year and quarter."

s = EdgarData('https://www.sec.gov/files/company_tickers.json')
print(s.annual_filing('0000320193', 2023))  # Annual filing for Apple Inc. in 2023
# print(s.quarterly_filing('0000320193', 2023, 1))  # Quarterly filing for Apple Inc. in Q1 2023

        
        
# s = EdgarData('https://www.sec.gov/files/company_tickers.json')
# print(s.ticker_to_cik("TSLA"))
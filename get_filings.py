import requests
import os
import re

import urllib.request
from bs4 import BeautifulSoup
from urllib.error import HTTPError


# AAPL CIK
cik = "320193"
# "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=10-k&dateb=20190101&owner=exclude&output=xml&count=100".format(cik)



def main():
    #ticker = input("Enter a ticker : ")
    ticker = "AAPL"
    
    #input_type = input("Enter the file type : ")
    input_type = "10-k"
    
    
    fp = open("data/tickers.txt") 
    ticker_list = fp.readlines()
    
    for ticker in ticker_list:
        ticker = ticker.strip('\n')
  
        cik_dict = getCIK(ticker)
        
        cik = cik_dict[ticker] 
        
        #print("The CIK for the inputted company |{0}| is |{1}|".format(ticker, cik)) 

        url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={0}&type={1}&dateb=20210101&owner=exclude&output=xml&count=100".format(cik, input_type)
        r = requests.get(url)
        data = r.text

        # Write the output of the request for testing
        # fp = open("testing.xml", "w+")
        # fp.write(data)
        # fp.close()

        path_dict = get_path_list(data)
        
        
        for date, path in path_dict.items():
            
            #print("|" + date + "|" + " -->  "+ path + "/Financial_Report.xlsx")
            if not os.path.exists('data/' + ticker):
                os.mkdir('data/' + ticker)
            
            if not os.path.exists('data/' + ticker + '/' + date):
                os.mkdir('data/' + ticker + '/' + date)
                os.mkdir('data/' + ticker + '/' + date + '/unprocessed')
                os.mkdir('data/' + ticker + '/' + date + '/processed')

            output_path = "data/" + ticker + "/" + date + "/unprocessed"

            try:
                urllib.request.urlretrieve(path + "/Financial_Report.xlsx", filename="{0}/{1}-{2}-{3}.xlsx".format(output_path, ticker, input_type.replace("-", ""), date))
            except HTTPError as err:
                try:
                    urllib.request.urlretrieve(path + "/Financial_Report.xls", filename="{0}/{1}-{2}-{3}.xls".format(output_path, ticker, input_type.replace("-", ""), date))
                except HTTPError as err:
                    print(err)



    
        
def get_path_list(data):
    # parse fetched data using BeautifulSoup
    soup = BeautifulSoup(data, features='lxml')
    
    path_dict = dict()

    for element in soup.find_all('filing'):
        if (element.find("xbrlref") != None):
            filing = element.find('filinghref')
            year = (element.find('datefiled').text)[:4]
            
            path = "/".join(filing.text.split("/")[:-1])
            
            path_dict[year] = path

    return path_dict


def getCIK(ticker):
    URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
    CIK_RE = re.compile(r'.*CIK=(\d{10}).*')
    cik_dict = {}
     
    f = requests.get(URL.format(ticker), stream = True)
    results = CIK_RE.findall(f.text)
    if len(results):
        results[0] = int(re.sub('\.[0]*', '.', results[0]))
        cik_dict[str(ticker).upper()] = str(results[0])
     
    f = open('cik_dict', 'w')
    f.close()

    return cik_dict


if __name__ == "__main__":
    main()




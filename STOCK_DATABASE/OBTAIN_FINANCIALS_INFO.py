import pandas as pd
import numpy as np
from urllib3 import HTTPResponse
from typing import cast
from polygon import RESTClient
import requests
import json
from datetime import datetime
from urllib3 import HTTPResponse
from typing import cast

filename="TOTAL_STOCK_LIST.csv"
stocks=pd.read_csv("/Users/milligil/STOCK_DATABASE/"+filename)
stocks=stocks.Symbol.tolist()
#stocks=["AAPL"]

apikey="5uYGSzAAq4YlD5n_omDUfSAbvYsKe3Yb"
timeframe="annual"
limit=100

timerlength=int(np.floor(len(stocks)/10))
counter=1

for stock in stocks:
    url=f'https://api.polygon.io/vX/reference/financials?ticker={stock}&filing_date.gte=2009-01-01&&timeframe={timeframe}&limit={limit}&apiKey={apikey}'

    content=requests.get(url=url).json()["results"]
    count=1
    final_content=[]

    for i in content:
        d={}
        d["Date"]=i["end_date"]
        
        i=i["financials"]
        balance_sheet=i["balance_sheet"]
        cash_flow_statement=i["cash_flow_statement"]
        comprehensive_income=i["comprehensive_income"]
        income_statement=i["income_statement"]
        
        for i in balance_sheet:
            value=balance_sheet[i]["value"]
            label=balance_sheet[i]["label"]
            d[label]=value
            
        for i in cash_flow_statement:
            value=cash_flow_statement[i]["value"]
            label=cash_flow_statement[i]["label"]
            d[label]=value
            
        for i in comprehensive_income:
            value=comprehensive_income[i]["value"]
            label=comprehensive_income[i]["label"]
            d[label]=value
            
        for i in income_statement:
            value=income_statement[i]["value"]
            label=income_statement[i]["label"]
            d[label]=value
        
        final_content.append(d)
        
    final_content=pd.DataFrame(final_content)
    
    try:
        final_content=final_content.set_index('Date')

        final_content=final_content.drop_duplicates()
        filename=f'{stock}.csv'
        final_content.to_csv("/Users/milligil/STOCK_DATABASE/FINANCIALS/"+filename)
    except:
        print(f'No data for {stock}')

    if counter % timerlength==0:
        print(str(int(counter/timerlength*10))+"%"+ " Complete")
    counter+=1


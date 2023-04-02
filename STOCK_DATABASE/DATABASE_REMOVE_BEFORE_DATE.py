import pandas as pd
from datetime import datetime

filename="TOTAL_STOCK_LIST.csv"
stocks=pd.read_csv("/Users/milligil/STOCK_DATABASE/"+filename)
stocks=stocks.Symbol.tolist()

stocks=["A"]

date_erase=datetime(2017,9,27)

for stock in stocks:
    filename=(str(stock)+".csv")
    data=pd.read_csv("/Users/milligil/STOCK_DATABASE/PRICES/"+filename)
    data["Date"]=pd.to_datetime(data["Date"])
    
    data=data[data.Date >= date_erase]
    
    data.to_csv("/Users/milligil/STOCK_DATABASE/PRICES/"+filename, index=False)
    
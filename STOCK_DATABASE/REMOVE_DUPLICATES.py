import pandas as pd
from datetime import datetime

filename="TOTAL_STOCK_LIST.csv"
stocks=pd.read_csv("/Users/milligil/STOCK_DATABASE/"+filename)
stocks=stocks.Symbol.tolist()

#stocks=["AAL"]

for stock in stocks:
    filename=(str(stock)+".csv")
    data=pd.read_csv("/Users/milligil/STOCK_DATABASE/PRICES/"+filename)
    data["Date"]=pd.to_datetime(data["Date"])
    
    length=len(data)-len(data.drop_duplicates())
    print(length)
    
    data=data.drop_duplicates()
    
    data.to_csv("/Users/milligil/STOCK_DATABASE/PRICES/"+filename, index=False)
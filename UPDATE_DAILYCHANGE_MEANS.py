import pandas as pd
import numpy as np

filename="TOTAL_STOCK_LIST.csv"
stocks=pd.read_csv("/Users/milligil/Desktop/STOCK_DATABASE/"+filename)
stocks=stocks.Symbol.tolist()
#stocks=["AAPL"]

total_df=[]

for stock in stocks:
    stock=stock.upper()
    filename=stock+".csv"

    historical_stock_price_df=pd.read_csv("/Users/milligil/Desktop/STOCK_DATABASE/PRICES/"+filename)
    historical_stock_price_df["Date"]=pd.to_datetime(historical_stock_price_df['Date'])
    historical_stock_price_df=historical_stock_price_df.set_index('Date')

    d={}
    d["Open"]=historical_stock_price_df["Open"].at_time('09:00')
    d["Close"]=historical_stock_price_df["Close"].at_time("15:30")
    diff_df=pd.DataFrame(d)

    #Good way to create daily stock dataframe.  You have to resample by day and remove NANs
    diff_df=diff_df.resample("D").mean()
    diff_df=diff_df.dropna()

    diff_df["Daily Difference"]=(diff_df["Close"]-diff_df["Open"])/diff_df["Open"]*100
    
    e={}
    e["Symbol"]=stock
    e["Mean (%)"]=diff_df["Daily Difference"].mean()
    e["Std Dev (%)"]=diff_df["Daily Difference"].std()
    
    total_df.append(e)

total_df=pd.DataFrame(total_df)
print(total_df)
filename="TOTAL_DAILY_CHANGE_AVERAGES.csv"
total_df.to_csv("/Users/milligil/Desktop/STOCK_DATABASE/DAILY_CHANGE_AVERAGES/"+filename, index=False)  

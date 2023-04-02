import pandas as pd
import numpy as np
from FUNCTIONS.PORTFOLIO import Portfolio as port
from FUNCTIONS.SIMULATOR_FUNCTIONS import SimulatorFunctions as simfunc
from FUNCTIONS.INDICATORS import Indicator as ind
from FUNCTIONS.GRAPHER import Grapher as graph
from datetime import timedelta, datetime, date
import scipy.stats as st
import matplotlib.pyplot as plt
from matplotlib.pyplot import scatter

startdate=datetime(2020, 1, 1)
enddate=datetime(2022, 10, 21)
currentdate=startdate

filename="TOTAL_DAILY_CHANGE_AVERAGES.csv"
daily_averages=pd.read_csv("/Users/milligil/STOCK_DATABASE/DAILY_CHANGE_AVERAGES/"+filename)
daily_averages=daily_averages.set_index("Symbol")

open_positions_df=pd.DataFrame()
transactions_df=pd.DataFrame()
balance_history_df=pd.DataFrame()
open_positions_df=pd.DataFrame()
counter=0

#filename="TOP_150.csv"
#stocks=pd.read_csv("/Users/milligil/Desktop/STOCK_DATABASE/"+filename)
#stocks=stocks.Symbol.tolist()
stocks=["AMC", "AAPL", "OCGN", "GME", "PYPL", "MSFT"]
#stocks=["GME"]

available_balance=10000
positionsize=1/len(stocks)
stoplosslimit=0.05
trailingstoplosslimit=0.04

daily_averages_df=[]
all_historical_stock_price_close_df=pd.DataFrame()
all_historical_stock_price_open_df=pd.DataFrame()
all_historical_stock_price_high_df=pd.DataFrame()
all_historical_stock_price_low_df=pd.DataFrame()

for stock in stocks:
    temp_historical_close_df=pd.DataFrame()
    temp_historical_open_df=pd.DataFrame()
    temp_historical_high_df=pd.DataFrame()
    temp_historical_low_df=pd.DataFrame()
    
    d={}    
    d["Stock"]=stock
    d["Mean (%)"]=daily_averages.at[stock, "Mean (%)"]
    d["Std Dev (%)"]=daily_averages.at[stock, "Std Dev (%)"]
    
    daily_averages_df.append(d)
    
    historical_stock_price_df=simfunc().get_historical_data(stock, startdate, enddate)
    
    temp_historical_close_df[stock]=historical_stock_price_df["Close"]
    temp_historical_open_df[stock]=historical_stock_price_df["Open"]
    temp_historical_high_df[stock]=historical_stock_price_df["High"]
    temp_historical_low_df[stock]=historical_stock_price_df["Low"]
    
    all_historical_stock_price_close_df=all_historical_stock_price_close_df.merge(temp_historical_close_df, left_index=True, right_index=True, how='outer')
    all_historical_stock_price_open_df=all_historical_stock_price_open_df.merge(temp_historical_open_df, left_index=True, right_index=True, how='outer')
    all_historical_stock_price_high_df=all_historical_stock_price_high_df.merge(temp_historical_high_df, left_index=True, right_index=True, how='outer')
    all_historical_stock_price_low_df=all_historical_stock_price_low_df.merge(temp_historical_low_df, left_index=True, right_index=True, how='outer')
    
daily_averages_df=pd.DataFrame(daily_averages_df)
daily_averages_df=daily_averages_df.set_index("Stock")

while currentdate.strftime("%Y-%m-%d") != (enddate+timedelta(days=1)).strftime("%Y-%m-%d"):
    
    if currentdate.strftime("%Y-%m-%d") in all_historical_stock_price_close_df.index:
        daily_prices_close_df=all_historical_stock_price_close_df.loc[currentdate.strftime("%Y-%m-%d")]
        if len(daily_prices_close_df)>0:
            daily_prices_open_df=all_historical_stock_price_open_df.loc[currentdate.strftime("%Y-%m-%d")]
            daily_prices_high_df=all_historical_stock_price_high_df.loc[currentdate.strftime("%Y-%m-%d")]
            daily_prices_low_df=all_historical_stock_price_low_df.loc[currentdate.strftime("%Y-%m-%d")]
        
            for stock in stocks:
                stock_daily_average=daily_averages_df.at[stock, "Mean (%)"]
                stock_daily_stddev=daily_averages_df.at[stock, "Std Dev (%)"]
                daily_stock_prices_df=pd.DataFrame()
                
                daily_stock_prices_df["Open"]=daily_prices_open_df[stock]
                daily_stock_prices_df["Close"]=daily_prices_close_df[stock]
                daily_stock_prices_df["High"]=daily_prices_high_df[stock]
                daily_stock_prices_df["Low"]=daily_prices_low_df[stock]
                
                current_open=daily_stock_prices_df["Open"][0]
                current_close=daily_stock_prices_df["Close"][-1]           
                diff=(current_close-current_open)/current_open*100     
                current_percentile=st.norm.cdf((diff-stock_daily_average)/stock_daily_stddev)*100
            
                if stock not in open_positions_df.index:
                    if current_percentile<5:
                        try:
                            tempdate=currentdate.strftime("%Y-%m-%d")    
                            stockbuy=port().stockbuy(tempdate, stock, current_close, positionsize, available_balance, open_positions_df)
                            available_balance=stockbuy[0]
                            open_positions_df=stockbuy[1]
                            open_positions_df["Stop Loss ($)"]=current_close*(1-stoplosslimit)
                                                    
                        except:
                            print(current_close, stock, available_balance, open_positions_df)
                            print(transactions_df)
                            print("Trade Failed on " + currentdate.strftime("%Y-%m-%d"))
                
                elif stock in open_positions_df.index:
                    open_positions_df.loc[stock,"Current Price ($)"]=current_close
                    
                    #Reset stoploss limit, TRAILING
                    open_positions_df=simfunc().stoploss_set(stock, current_close, stoplosslimit, "Yes", trailingstoplosslimit, open_positions_df)
                    
                    if simfunc().stoplosscheck(stock, current_close,open_positions_df)=="Yes":
                        try:
                            tempdate=currentdate.strftime("%Y-%m-%d")
                            stocksell=port().stocksell(open_positions_df, tempdate, stock, current_close, available_balance)
                            available_balance=stocksell[0]
                            transactions_df=transactions_df.append(stocksell[1])
                            open_positions_df=stocksell[2]                                          
                        except:
                            print("Sell Failed on " + currentdate.strftime("%Y-%m-%d"))  
                             
                if currentdate.strftime("%Y-%m-%d")==enddate.strftime("%Y-%m-%d") and len(open_positions_df)>=1:
                    tempdate=currentdate.strftime("%Y-%m-%d")
                    for stock in open_positions_df:
                        stocksell=port().stocksell(open_positions_df, tempdate, stock, current_close, available_balance)
                        transactions_df=transactions_df.append(stocksell[1])
                        open_positions_df=stocksell[2]
                    
    if len(open_positions_df)>=1:
        balance_history_df=simfunc().updatebalance(currentdate, open_positions_df, available_balance, balance_history_df)
    else:
        balance_history_df=simfunc().updatebalance_no_open(currentdate, available_balance, balance_history_df)
      
    currentdate=currentdate+timedelta(days=1)
    counter+=1
    
balance_history_df=balance_history_df.set_index("Date")
transactions_df=transactions_df.reset_index()
del transactions_df["index"]
#print(transactions_df.sort_values(by=['Net (%)']))
print(transactions_df.to_string())

trade_avg_by_stock_df=pd.DataFrame()
for stock in stocks:
    trade_avg_by_stock_df[stock]=transactions_df.loc

algo_stats=simfunc().calculate_strategy_stats(startdate, enddate, balance_history_df, transactions_df)
benchmarks_df=simfunc().calculate_benchmarks(startdate, enddate, balance_history_df)

graph().benchmarks(benchmarks_df)
if len(stocks)<2:
    graph().trade_plot(stock, transactions_df, all_historical_stock_price_close_df)
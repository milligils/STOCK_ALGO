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

available_balance=10000
positionsize=0.2
stoplosslimit=0.05
trailingstoplosslimit=0.04

startdate=datetime(2020, 1, 1)
enddate=datetime(2022, 10, 21)
currentdate=startdate
bar_interval="5Min"

#4H intervals, bollinger bands converted to 8H to approximate 20D. 
sma_interval=2*4
sma_short_duration=20
sma_med_duration=50
sma_long_duration=200

open_positions_df=pd.DataFrame()
transactions_df=pd.DataFrame()
balance_history_df=pd.DataFrame()
open_positions_df=pd.DataFrame()
counter=0

stocks=["AMD", "AAPL", "GE", "F", "ABNB", "MSFT"]
#stocks=["AMD"]

all_historical_stock_price_close_df=pd.DataFrame()
all_historical_stock_price_open_df=pd.DataFrame()
all_historical_stock_price_high_df=pd.DataFrame()
all_historical_stock_price_low_df=pd.DataFrame()

for stock in stocks:
    temp_historical_close_df=pd.DataFrame()
    temp_historical_open_df=pd.DataFrame()
    temp_historical_high_df=pd.DataFrame()
    temp_historical_low_df=pd.DataFrame()
    
    historical_stock_price_df=simfunc().get_historical_data(stock, startdate, enddate)
    historical_stock_price_df=simfunc().change_bar_interval(historical_stock_price_df,bar_interval)
    
    temp_historical_close_df[stock]=historical_stock_price_df["Close"]
    temp_historical_open_df[stock]=historical_stock_price_df["Open"]
    temp_historical_high_df[stock]=historical_stock_price_df["High"]
    temp_historical_low_df[stock]=historical_stock_price_df["Low"]
    
    all_historical_stock_price_close_df=all_historical_stock_price_close_df.merge(temp_historical_close_df, left_index=True, right_index=True, how='outer')
    all_historical_stock_price_open_df=all_historical_stock_price_open_df.merge(temp_historical_open_df, left_index=True, right_index=True, how='outer')
    all_historical_stock_price_high_df=all_historical_stock_price_high_df.merge(temp_historical_high_df, left_index=True, right_index=True, how='outer')
    all_historical_stock_price_low_df=all_historical_stock_price_low_df.merge(temp_historical_low_df, left_index=True, right_index=True, how='outer')
    
    #SMA DATA
    historical_stock_price_df=ind().sma(sma_short_duration, sma_interval, historical_stock_price_df)
    historical_stock_price_df=ind().sma(sma_med_duration, sma_interval, historical_stock_price_df)
    historical_stock_price_df=ind().sma(sma_long_duration, sma_interval, historical_stock_price_df)
    historical_stock_price_df=ind().sma_diff("Close", f'SMA {sma_long_duration}',historical_stock_price_df)
    historical_stock_price_df=ind().bollinger(sma_short_duration, historical_stock_price_df)

while currentdate.strftime("%Y-%m-%d") != (enddate+timedelta(days=1)).strftime("%Y-%m-%d"):
    
    if currentdate.strftime("%Y-%m-%d") in all_historical_stock_price_close_df.index:
        daily_prices_close_df=all_historical_stock_price_close_df.loc[currentdate.strftime("%Y-%m-%d")]
        if len(daily_prices_close_df)>0:
            daily_prices_open_df=all_historical_stock_price_open_df.loc[currentdate.strftime("%Y-%m-%d")]
            daily_prices_high_df=all_historical_stock_price_high_df.loc[currentdate.strftime("%Y-%m-%d")]
            daily_prices_low_df=all_historical_stock_price_low_df.loc[currentdate.strftime("%Y-%m-%d")]
        
            for stock in stocks:
                daily_stock_prices_df=pd.DataFrame()
                
                daily_stock_prices_df["Open"]=daily_prices_open_df[stock]
                daily_stock_prices_df["Close"]=daily_prices_close_df[stock]
                daily_stock_prices_df["High"]=daily_prices_high_df[stock]
                daily_stock_prices_df["Low"]=daily_prices_low_df[stock]
                
                current_open=daily_stock_prices_df["Open"][0]
                current_close=daily_stock_prices_df["Close"][-1]           
                diff=(current_close-current_open)/current_open*100     
                
            
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
print(transactions_df)

algo_stats=simfunc().calculate_strategy_stats(startdate, enddate, balance_history_df, transactions_df)
benchmarks_df=simfunc().calculate_benchmarks(startdate, enddate, balance_history_df)

graph().benchmarks(benchmarks_df)
if len(stocks)<2:
    graph().trade_plot(stock, transactions_df, all_historical_stock_price_close_df)
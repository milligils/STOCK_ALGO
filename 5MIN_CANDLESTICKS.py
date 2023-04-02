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
from FUNCTIONS.CANDLESTICKS import Candlesticks as candle

available_balance=10000
positionsize=0.2
stoplosslimit=0.05
trailingstoplosslimit=0.04

startdate=datetime(2022, 5, 1)
enddate=datetime(2023, 2, 4)
currentdate=startdate
bar_interval="5Min"

open_positions_df=pd.DataFrame()
transactions_df=pd.DataFrame()
balance_history_df=pd.DataFrame()
open_positions_df=pd.DataFrame()
counter=0

stocks=["AMD", "AAPL", "GE", "F", "ABNB", "MSFT"]
#stocks=["AAPL"]

all_historical_stock_price_close_df=simfunc().combine_stock_data_change_interval(stocks, startdate, enddate, "Close", bar_interval)
all_historical_stock_price_open_df=simfunc().combine_stock_data_change_interval(stocks, startdate, enddate, "Open", bar_interval)
all_historical_stock_price_high_df=simfunc().combine_stock_data_change_interval(stocks, startdate, enddate, "High", bar_interval)
all_historical_stock_price_low_df=simfunc().combine_stock_data_change_interval(stocks, startdate, enddate, "Low", bar_interval)
   
while currentdate.strftime("%Y-%m-%d") != (enddate+timedelta(days=1)).strftime("%Y-%m-%d"):
    
    if currentdate.strftime("%Y-%m-%d") in all_historical_stock_price_close_df.index:
        daily_prices_close_df=all_historical_stock_price_close_df.loc[currentdate.strftime("%Y-%m-%d")]
        daily_prices_high_df=all_historical_stock_price_high_df.loc[currentdate.strftime("%Y-%m-%d")]
        daily_prices_low_df=all_historical_stock_price_low_df.loc[currentdate.strftime("%Y-%m-%d")]
        daily_prices_open_df=all_historical_stock_price_open_df.loc[currentdate.strftime("%Y-%m-%d")]
        
        for i in daily_prices_close_df.index:
            for stock in stocks:
                current_close=daily_prices_close_df[stock].loc[i]
                current_open=daily_prices_open_df[stock].loc[i]
                current_low=daily_prices_low_df[stock].loc[i]
                current_high=daily_prices_high_df[stock].loc[i]
                
                if stock not in open_positions_df.index:
                    test=candle().hammer(current_open, current_close, current_high, current_low)
                    
                    if test=="Yes":
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
                    
                #Close open positions at end            
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
#if len(stocks)<2:
    #graph().candlestick_plus_trades(stock, startdate, enddate, historical_stock_price_df, transactions_df)
    
    
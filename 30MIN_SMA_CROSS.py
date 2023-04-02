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
enddate=datetime(2023, 2, 3)
currentdate=startdate
bar_interval="30Min"

#4H intervals, bollinger bands converted to 8H to approximate 20D. 
sma_interval=4
sma_long_duration=200
sma_med_duration=50

open_positions_df=pd.DataFrame()
transactions_df=pd.DataFrame()
balance_history_df=pd.DataFrame()
open_positions_df=pd.DataFrame()
counter=0

filename="TOTAL_STOCK_LIST.csv"
stocks=pd.read_csv("/Users/milligil/STOCK_DATABASE/"+filename)
stocks=stocks.Symbol.tolist()
stocks=["AMD", "AAPL", "GE", "MSFT"]
#stocks=["MSFT", "AAPL", "GOOG"]

available_balance=10000
positionsize=1/len(stocks)
stoplosslimit=0.07
trailingstoplosslimit=0.1

all_historical_stock_price_close_df=pd.DataFrame()
sma_long_df=pd.DataFrame()
sma_med_df=pd.DataFrame()

for stock in stocks:
    temp_historical_close_df=pd.DataFrame()
    
    historical_stock_price_df=simfunc().get_historical_data(stock, startdate, enddate)
    historical_stock_price_df=simfunc().change_bar_interval(historical_stock_price_df,bar_interval)
    
    temp_historical_close_df[stock]=historical_stock_price_df["Close"]
    all_historical_stock_price_close_df=all_historical_stock_price_close_df.merge(temp_historical_close_df, left_index=True, right_index=True, how='outer')
    
    #SMA DATA
    historical_stock_price_df=ind().sma(sma_long_duration,sma_interval, historical_stock_price_df)
    historical_stock_price_df=ind().sma(sma_med_duration,sma_interval, historical_stock_price_df)
    
    sma_long_df[stock]=historical_stock_price_df[f'SMA {sma_long_duration:.0f}']
    sma_med_df[stock]=historical_stock_price_df[f'SMA {sma_med_duration:.0f}']
    
sma_long_df=sma_long_df.dropna()
sma_med_df=sma_med_df.dropna()
    
while currentdate.strftime("%Y-%m-%d") != (enddate+timedelta(days=1)).strftime("%Y-%m-%d"):
    
    if currentdate.strftime("%Y-%m-%d") in sma_long_df.index:
        daily_prices_close_df=all_historical_stock_price_close_df.loc[currentdate.strftime("%Y-%m-%d")]
        
        for i in daily_prices_close_df.index:
            if i in sma_long_df.index:
                for stock in stocks:
                    current_close=daily_prices_close_df[stock].loc[i]
                    current_sma_long=sma_long_df[stock].loc[i]
                    current_sma_med=sma_med_df[stock].loc[i]
                    
                    if stock not in open_positions_df.index:
                        if current_close>current_sma_long and current_sma_med<current_sma_long:
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
#print(transactions_df)
print(transactions_df.to_string())

algo_stats=simfunc().calculate_strategy_stats(startdate, enddate, balance_history_df, transactions_df)
benchmarks_df=simfunc().calculate_benchmarks(startdate, enddate, balance_history_df)

graph().benchmarks(benchmarks_df)
for stock in stocks:
    temp_price=pd.DataFrame()
    temp_sma=pd.DataFrame()
    try:
        stock_transactions_df=transactions_df.loc[transactions_df["Stock"]==stock]
        temp_price[stock]=all_historical_stock_price_close_df[stock]
        temp_sma[stock]=sma_long_df[stock]
        graph().sma_price_trades(stock, stock_transactions_df, temp_price, temp_sma)
    except:
        pass
    
    
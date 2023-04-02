from SQL_OPERATIONS import SQLOps as so

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date, datetime, timedelta, time
import pandas_market_calendars as mycal

nyse=mycal.get_calendar('NYSE')
calendar=nyse.schedule(start_date="2022-01-01", end_date="2022-12-31")
calendar=mycal.date_range(calendar,frequency="1D")
calendar=calendar.strftime('%Y-%m-%d')

today=date.today()
today=today.strftime('%Y-%m-%d')

if today in calendar:
    db="stock_prices"
    tablename="Stocks"
    columnname="Symbol"
    
    period=30
    periodtype="minute"
    start="2021-10-01"
    end="2021-11-30"
    
    SQLOp=so()
    stocks=SQLOp.obtain_data(db, columnname, tablename)
    
    timerlength=int(np.floor(len(stocks)/10))
    counter=1
    columnnames=(   "CalendarDay, "
                    "TimeofDay, "
                    "Open_Price, "
                    "High_Price, "
                    "Low_Price, "
                    "Close_Price, "
                    "Volume, "
                )
    
    for stock in stocks:        
        SQLOp.upload_new_prices(stock, columnnames, period, periodtype, start, end)
        
        if counter % timerlength==0:
            print(str(int(counter/timerlength*10))+"%"+ " Complete")
        counter+=1
        
else:
    print("Stock Market Closed")
    
import pandas as pd
import yfinance as yf
import numpy as np
import alpaca_trade_api as tradeapi
import requests
import json
from datetime import datetime
import time
from polygon import RESTClient
from urllib3 import HTTPResponse
from typing import cast

class StockInfo():
    def __init__(self):
        self.AlpacaOn = False
        self.yfOn = False
        self.TDAOn = False
        self.polyOn=False
        self.ticker_df = []
        self.date_df = []
        
    def get_prices_yf(self, stock, period, interval):
        self.stock=stock
        self.period = period
        self.interval = interval
        ticker = yf.Ticker(self.stock)    
        
        ticker_df = pd.DataFrame(ticker.history(period=self.period, interval=self.interval))   
        ticker_df = ticker_df[::-1]
        ticker_df.reset_index(inplace=True)
        del ticker_df["Stock Splits"]
        del ticker_df["Dividends"]
        
        print(ticker_df)
        
        ticker_df.columns=["Date", "Open", "High", "Low", "Close","Volume"]
        ticker_df = ticker_df.replace(0,np.nan)
        self.yfOn = not self.yfOn
        return ticker_df
    
    def get_prices_alpaca(self, stock, start, end, alpaca_timeframe):
        self.stock=stock
        self.start=start
        self.end=end
        self.alpaca_timeframe=alpaca_timeframe
        
        SEC_KEY = 'MXV7IeSnnmPtcQ1QhnZyk4Zcv2dE4rsbjt8K8yFv' # Enter Your Secret Key Here
        PUB_KEY = 'PK5YBZ21JNUZFDN2DXWO' # Enter Your Public Key Here
        BASE_URL = 'https://paper-api.alpaca.markets' # This is the base URL for paper trading
        api = tradeapi.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

        ticker = api.get_bars(self.stock, alpaca_timeframe, start, end)
        
        for bar in ticker:
            self.ticker_df.append(bar.c)
            current_date = bar.t
            current_date = current_date.strftime('%Y-%m-%d')
            self.date_df.append(current_date)
        
        ticker_df = {'Date': self.date_df, 'Close': self.ticker_df}
        ticker_df = pd.DataFrame(ticker_df)[::-1]
        ticker_df.reset_index(inplace=True)
        del ticker_df['index']
        ticker_df.columns=["Date", "Price"]
        self.AlpacaOn = not self.AlpacaOn
        return ticker_df
    
    def get_prices_tda(self, stock, period, periodtype, frequency, frequencytype):
        self.stock=stock
        self.period=period
        self.periodtype=periodtype
        self.frequency=frequency
        self.frequencytype=frequencytype
        
        td_consumer_key = 'O6FTNTFGCZFIWTWBXDN7JSZBYETPRI66'

        endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?apikey={apikey}&periodType={periodtype}&period={period}&frequencyType={frequencyType}&frequency={frequency}&needExtendedHoursData=false'
        full_url = endpoint.format(stock_ticker=stock, period=period_tda, periodtype=periodtype_tda, frequency=frequency_tda, frequencyType=frequencytype_tda, apikey=td_consumer_key)
        page = requests.get(url=full_url, params={'apikey': td_consumer_key})
        content = json.loads(page.content)['candles']

        #print(content)
        
        for i in content:
            d={}
            d["Date"]=datetime.fromtimestamp(int(i["datetime"]/1000))
            d["High"]=i["high"]
            d["Low"]=i["low"]
            d["Open"]=i["open"]
            d["Close"]=i["close"]
            d["Volume"]=i["volume"]
            
            self.ticker_df.append(d)
            
        ticker_df=pd.DataFrame(self.ticker_df)[::-1]
        ticker_df.reset_index(inplace=True)
        del ticker_df["index"]
        ticker_df=ticker_df[["Date", "Open", "High", "Low", "Close","Volume"]]
        
        self.TDAOn = not self.TDAOn
        return ticker_df
    
    def get_prices_polygon(self, stock, period, periodtype, start, end):
        self.stock=stock
        self.period=period
        self.periodtype=periodtype
        self.start=start
        self.end=end
        
        apikey="5uYGSzAAq4YlD5n_omDUfSAbvYsKe3Yb"
        
        client=RESTClient(api_key=apikey)
        aggs=cast(HTTPResponse, client.get_aggs(self.stock, self.period, self.periodtype, self.start, self.end, sort="desc", raw=True, adjusted=True, limit=50000))
        content=json.loads(aggs.data.decode(("utf-8")))["results"]

        for i in content:
            d={}
            d["Date"]=datetime.fromtimestamp(int(i["t"]/1000))
            d["High"]=i["h"]
            d["Low"]=i["l"]
            d["Open"]=i["o"]
            d["Close"]=i["c"]
            d["Volume"]=i["v"]
            
            self.ticker_df.append(d)
            
        ticker_df=pd.DataFrame(self.ticker_df)
        ticker_df.reset_index(inplace=True)
        del ticker_df["index"]
        ticker_df=ticker_df[["Date", "Open", "High", "Low", "Close","Volume"]]
        
        self.polyOn=True
        return ticker_df

if __name__ == '__main__':
    
    period_yf = "6mo"
    interval_yf = "1h"
    start="2020-01-01"
    end="2020-12-04"
    alpaca_timeframe = "1Hour"
    period_tda = 2
    periodtype_tda = "day"
    frequencytype_tda = "minute"
    frequency_tda = 15
    period_poly=5
    periodtype_poly="minute"
    
    stock = "BAC"
    
    stockinfo = StockInfo()
    #info = stockinfo.get_prices_alpaca(stock, start, end,alpaca_timeframe)
    ##print(info)
    #info2 = stockinfo.get_prices_yf(stock, period_yf, interval_yf)
    ##print(info2)
    #info3 = stockinfo.get_prices_tda(stock, period_tda, periodtype_tda, frequency_tda, frequencytype_tda)
    #print(info3)
    
    info4=stockinfo.get_prices_polygon(stock,period_poly, periodtype_poly, start, end)
    print(info4)

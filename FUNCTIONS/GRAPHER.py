import pandas as pd
import numpy as np
from datetime import timedelta, datetime, date
import scipy.stats as st
import matplotlib.pyplot as plt
from matplotlib.pyplot import scatter

class Grapher(object):
    def __init__(self):
        pass
    
    def stock_price(self, stock, startdate, enddate, stockdata):
        self.stock=stock
        self.startdate=startdate
        self.enddate=enddate
        self.stockdata=stockdata
        
        stockdata=stockdata.reset_index()
        stockdata["Date"]=pd.to_datetime(stockdata['Date'])    
        
        stockdata.plot('Date', "Close")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.title(stock)
        plt.show()
        
    def candlestick (self, stock, startdate, enddate, stockdata):
        self.stock=stock
        self.startdate=startdate
        self.enddate=enddate
        self.stockdata=stockdata
        
        startdate=pd.to_datetime(self.startdate)
        enddate=pd.to_datetime(self.enddate)
        
        stockdata=stockdata.reset_index()
        stockdata["Date"]=pd.to_datetime(stockdata['Date'])
        stockdata["Diff"]=stockdata["Date"].diff(1)
        minutebars=stockdata["Diff"][1].total_seconds()/60
        
        stockdata=stockdata.set_index("Date")
        
        plt.figure()
        
        width=pd.Timedelta(minutes=(minutebars/2))
        width2=width/5
        
        print(stockdata)
        print(type(stockdata))
        up=stockdata[stockdata["Close"]>=stockdata["Open"]]
        down=stockdata[stockdata["Close"]<stockdata["Open"]]
        
        color1="green"
        color2="red"
        
        #plot up prices
        plt.bar(up.index, up["Close"]-up["Open"], width, bottom=up["Open"], color=color1)
        plt.bar(up.index, up["High"]-up["Close"], width2, bottom=up["Close"], color=color1)
        plt.bar(up.index, up["Low"]-up["Open"], width2, bottom=up["Open"], color=color1)
        
        #plot down prices
        plt.bar(down.index, down["Close"]-down["Open"], width, bottom=down["Open"], color=color2)
        plt.bar(down.index, down["High"]-down["Open"], width2, bottom=down["Open"], color=color2)
        plt.bar(down.index, down["Low"]-down["Close"], width2, bottom=down["Close"], color=color2)
        
        plt.xticks(rotation=45, ha="right")
        
        plt.show()
        
    def candlestick_plus_trades(self, stock, startdate, enddate, stockdata, transactions_df):
        self.stock=stock
        self.startdate=startdate
        self.enddate=enddate
        self.stockdata=stockdata
        self.transactions_df=transactions_df
        
        startdate=pd.to_datetime(self.startdate)
        enddate=pd.to_datetime(self.enddate)
        
        stockdata=stockdata.reset_index()
        stockdata["Date"]=pd.to_datetime(stockdata['Date'])
        stockdata["Diff"]=stockdata["Date"].diff(1)
        minutebars=stockdata["Diff"][1].total_seconds()/60
        
        stockdata=stockdata.set_index("Date")
        
        transactions_df["Date Opened"]=pd.to_datetime(transactions_df["Date Opened"])
        transactions_df["Date Sold"]=pd.to_datetime(transactions_df["Date Sold"])
        
        plt.figure()
        
        width=pd.Timedelta(minutes=(minutebars/2))
        width2=width/5
        
        print(stockdata)
        print(type(stockdata))
        up=stockdata[stockdata["Close"]>=stockdata["Open"]]
        down=stockdata[stockdata["Close"]<stockdata["Open"]]
        
        print(up)
        print(down)
        
        color1="green"
        color2="red"
        
        #plot up prices
        ax=plt.bar(up.index, up["Close"]-up["Open"], width, bottom=up["Open"], color=color1)
        plt.bar(up.index, up["High"]-up["Close"], width2, bottom=up["Close"], color=color1, ax=ax)
        plt.bar(up.index, up["Low"]-up["Open"], width2, bottom=up["Open"], color=color1, ax=ax)
        
        #plot down prices
        plt.bar(down.index, down["Close"]-down["Open"], width, bottom=down["Open"], color=color2, ax=ax)
        plt.bar(down.index, down["High"]-down["Open"], width2, bottom=down["Open"], color=color2, ax=ax)
        plt.bar(down.index, down["Low"]-down["Close"], width2, bottom=down["Close"], color=color2, ax=ax)
        
        transactions_df.plot(x='Date Opened', y="Price Bought ($)", marker="^", color="black", linestyle="", ax=ax)
        transactions_df.plot(x='Date Sold', y="Price Sold ($)", marker="v", color="black", linestyle="", ax=ax)

        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.show()
    
    def trade_plot(self, stock, transactions_df, historical_stock_price_data):
        self.transactions_df=transactions_df
        self.historical_stock_price_data=historical_stock_price_data
        self.stock=stock
        
        transactions_df["Date Opened"]=pd.to_datetime(transactions_df["Date Opened"])
        transactions_df["Date Sold"]=pd.to_datetime(transactions_df["Date Sold"])
        historical_stock_price_data["Date"]=historical_stock_price_data.index

        ax=historical_stock_price_data.plot(x="Date", y=stock, color="blue")
        transactions_df.plot(x='Date Opened', y="Price Bought ($)", marker="^", color="green", linestyle="", ax=ax)
        transactions_df.plot(x='Date Sold', y="Price Sold ($)", marker="v", color="red", linestyle="", ax=ax)

        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.show()
        
    def benchmarks(self, benchmarks_df):
        self.benchmarks_df=benchmarks_df
        
        benchmarks_df=benchmarks_df.reset_index()
        benchmarks_y=["Portfolio %", "SPY %", "QQQ %"]
        benchmarks_df.plot('index', y=benchmarks_y)
        plt.xticks(rotation=90)
        plt.xlabel("Date")
        plt.ylabel("Percent Change in Portfolio (%)")
        plt.show()
    
    def multi_date(self, y_array, data):
        self.y_array=y_array
        self.data=data
        
        data=data.reset_index()
        data["Date"]=pd.to_datetime(data['Date']) 
        data.plot("Date", y=y_array)
        plt.show()
        
    
       
    def sma_price_trades(self, stock, transactions_df, historical_stock_price_data, sma_array):
        self.stock=stock
        self.trades_df=transactions_df
        self.historical_stock_price_data=historical_stock_price_data
        self.sma_array=sma_array
        
        transactions_df["Date Opened"]=pd.to_datetime(transactions_df["Date Opened"])
        transactions_df["Date Sold"]=pd.to_datetime(transactions_df["Date Sold"])
        historical_stock_price_data=historical_stock_price_data.reset_index()
        sma_array=sma_array.reset_index()
        
        ax=historical_stock_price_data.plot(x="Date", y=stock, color="blue")
        sma_array.plot(x="Date", y=stock, color="orange", label=f'{stock} SMA', ax=ax)
        transactions_df.plot(x='Date Opened', y="Price Bought ($)", marker="^", color="green", linestyle="", ax=ax)
        transactions_df.plot(x='Date Sold', y="Price Sold ($)", marker="v", color="red", linestyle="", ax=ax)

        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.show()


if __name__ == '__main__':         
    import pandas as pd
    import numpy as np
    #from FUNCTIONS.PORTFOLIO import Portfolio as port
    from SIMULATOR_FUNCTIONS import SimulatorFunctions as simfunc
    #from FUNCTIONS.INDICATORS import Indicator as ind
    from datetime import timedelta, datetime, date
    import scipy.stats as st
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import scatter
    
    stock="AMZN"
    filename=f'{stock}.csv'
    start="2020-01-01"
    end="2023-02-04"
   
    stockdata=simfunc().get_historical_data(stock, start, end)
    #Grapher().stock_price(stock,start,end, stockdata)
    
    stocks=["AMD", "AAPL", "GE", "F", "ABNB", "MSFT"]
    all_historical_stock_price_close_df=pd.DataFrame()

    for stock in stocks:
        temp_historical_close_df=pd.DataFrame()
        
        historical_stock_price_df=simfunc().get_historical_data(stock, start, end)
        temp_historical_close_df[stock]=historical_stock_price_df["Close"]
        all_historical_stock_price_close_df=all_historical_stock_price_close_df.merge(temp_historical_close_df, left_index=True, right_index=True, how='outer')
        
    Grapher().multi_date(stocks,all_historical_stock_price_close_df)
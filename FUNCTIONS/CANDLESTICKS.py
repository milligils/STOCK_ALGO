class Candlesticks(object):
    def __init__(self):
        pass
    
    def hammer(self, open, close, high, low):
        self.open=open
        self.close=close
        self.high=high
        self.low=low
        
        if close>open and open>((high-low)*0.75+low):
            candlestick_check="Yes"
        else:
            candlestick_check="No"
            
        return candlestick_check
    
    def hangingman(self, open, close, high, low):
        self.open=open
        self.close=close
        self.high=high
        self.low=low
        
        if close<open and close>((high-low)*0.75+low):
            candlestick_check="Yes"
        else:
            candlestick_check="No"
            
        return candlestick_check
        
        



if __name__ == '__main__':  
    import pandas as pd
    import numpy as np
    from PORTFOLIO import Portfolio as port
    from SIMULATOR_FUNCTIONS import SimulatorFunctions as simfunc
    from INDICATORS import Indicator as ind
    from datetime import timedelta, datetime, date
    import scipy.stats as st
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import scatter
    import plotly.graph_objects as go
    
    historical_stock_price_df=[]
    
    startdate=datetime(2022, 1,1)
    high=100
    low=95
    open=(high-low)*0.7+low
    close=open*1.01
    
    open=100
    close=97
    high=101
    low=80
    
    
    d={}
    d["Date"]=startdate
    d["Open"]=open
    d["Close"]=close
    d["Low"]=low
    d["High"]=high
    
    historical_stock_price_df.append(d)
    historical_stock_price_df=pd.DataFrame(historical_stock_price_df)
    print(historical_stock_price_df)
    print(Candlesticks().hammer(open, close, high, low))
    print(Candlesticks().hangingman(open, close, high, low))
    
    plt.figure()
    
    width=0.4
    width2=0.05
    
    up=historical_stock_price_df[historical_stock_price_df["Close"]>=historical_stock_price_df["Open"]]
    down=historical_stock_price_df[historical_stock_price_df["Close"]<historical_stock_price_df["Open"]]
    
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
    
    
    
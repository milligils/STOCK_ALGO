class Indicator(object):
    def __init__(self):
        pass
    
    def bollinger(self, sma_short_duration, historical_stock_price_df):
        self.historical_stock_price_df=historical_stock_price_df
        self.sma_short_duration=sma_short_duration
        
        historical_stock_price_df['Bollinger Upper']=historical_stock_price_df["Close"].rolling(window=sma_short_duration*2).mean()+historical_stock_price_df["Close"].rolling(window=sma_short_duration*2).std()
        historical_stock_price_df['Bollinger Lower']=historical_stock_price_df["Close"].rolling(window=sma_short_duration*2).mean()-historical_stock_price_df["Close"].rolling(window=sma_short_duration*2).std()

        return historical_stock_price_df 
        
    def rsi(self, rsi_duration, historical_stock_price_df):
        self.rsi_duration=rsi_duration
        self.historical_stock_price_df=historical_stock_price_df
        
        rsi_delta=historical_stock_price_df["Close"].diff()
        rsi_up=rsi_delta.clip(lower=0)
        rsi_down=-1*rsi_delta.clip(upper=0)
        
        ma_up=rsi_up.rolling(window=rsi_duration).mean()
        ma_down=rsi_down.rolling(window=rsi_duration).mean()
        
        rsi=ma_up/ma_down
        
        duration_length=rsi_duration/15
        
        historical_stock_price_df[f'RSI {duration_length:.0f} days']=100-(100/(1+rsi))
        
        return historical_stock_price_df
        
    def sma(self, duration, sma_interval, historical_stock_price_df):
        self.duration=duration
        self.sma_interval=sma_interval
        self.historical_stock_price_df=historical_stock_price_df
        
        sma_duration=duration*sma_interval
        
        historical_stock_price_df[f'SMA {duration:.0f}']=historical_stock_price_df["Close"].rolling(sma_duration).mean()
                
        return historical_stock_price_df
    
    def sma_diff(self, shortterm, longterm, historical_stock_price_df):
        self.shortterm=shortterm
        self.longterm=longterm
        self.historical_stock_price_df=historical_stock_price_df
                
        historical_stock_price_df[f'{shortterm}/{longterm} Diff']=(historical_stock_price_df[f'{shortterm}']-historical_stock_price_df[f'{longterm}'])/historical_stock_price_df[f'{longterm}']
        
        return historical_stock_price_df
    
    def atr(self, duration, historical_stock_price_df):
        self.duration=duration
        self.historical_stock_price_df=historical_stock_price_df
    
        high_low=historical_stock_price_df["High"]-historical_stock_price_df["Low"]
        high_close=np.abs(historical_stock_price_df["High"]-historical_stock_price_df["Close"].shift())
        low_close=np.abs(historical_stock_price_df["Low"]-historical_stock_price_df["Close"].shift())
        ranges=pd.concat([high_low, high_close, low_close], axis=1)
        true_range=np.max(ranges, axis=1)
        historical_stock_price_df["ATR"]=true_range.rolling(duration).sum()/duration
            
        return historical_stock_price_df
    
    def rel_volume(self, duration, historical_stock_price_df):
        self.duration=duration
        self.historical_stock_price_df=historical_stock_price_df
        duration_length=duration/14
        
        historical_stock_price_df[f'Avg. Volume {duration_length:.0f} days']=historical_stock_price_df["Volume"].rolling(window=duration).mean()                

        return historical_stock_price_df
        
if __name__ == '__main__':   
    import pandas as pd
    import numpy as np
    #from datetime import date, timedelta, datetime
    import matplotlib.pyplot as plt
    from SIMULATOR_FUNCTIONS import SimulatorFunctions as simfunc

    stock="AAL"
    start = "2020-07-01"
    end = "2022-12-10"
    #4H intervals, bollinger bands converted to 8H to approximate 20D. 
    sma_interval=2*4
    sma_short_duration=20
    sma_med_duration=50
    sma_long_duration=200
    atr_duration=15*14
    rsi_duration=15*7
    
    historical_stock_price_df=simfunc().get_historical_data(stock, start, end)
    
    historical_stock_price_df=Indicator().sma(sma_long_duration, sma_interval, historical_stock_price_df)
    historical_stock_price_df=Indicator().sma(sma_med_duration, sma_interval, historical_stock_price_df)
    historical_stock_price_df=Indicator().sma(sma_short_duration, sma_interval, historical_stock_price_df)
    historical_stock_price_df=Indicator().sma_diff("Close", "SMA 200", historical_stock_price_df)
    historical_stock_price_df=Indicator().bollinger(sma_short_duration, historical_stock_price_df)
    historical_stock_price_df=Indicator().rel_volume(14*365, historical_stock_price_df)
    historical_stock_price_df=Indicator().rel_volume(14*7, historical_stock_price_df)
    historical_stock_price_df=Indicator().rsi(rsi_duration, historical_stock_price_df)
    print(historical_stock_price_df)
    
    historical_stock_price_df=Indicator().atr(atr_duration, historical_stock_price_df)
      
    fig, ax1=plt.subplots()
    ax2=ax1.twinx()
    ax1.plot(historical_stock_price_df.index, historical_stock_price_df["Close"], color="blue")
    ax2.plot(historical_stock_price_df.index, historical_stock_price_df["SMA 200"],  color="green")
    plt.show()




    

        


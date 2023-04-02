import pandas as pd
import numpy as np 
from dateutil.relativedelta import relativedelta
from calendar import isleap

class SimulatorFunctions (object):
    def __init__(self):
        pass
    
    def calculate_benchmarks (self, startdate, enddate, balance_history_df):
        self.startdate=startdate
        self.enddate=enddate
        self.balance_history_df=balance_history_df
        
        benchmarks_df=pd.DataFrame()
        temp_df=pd.DataFrame()
        stocks=["SPY", "QQQ"]
        
        benchmarks_df["Portfolio"]=balance_history_df["Balance"]
                
        for stock in stocks:
            stock_price_df=SimulatorFunctions().get_historical_data(stock, startdate, enddate)
            temp_df[stock]=stock_price_df[(stock_price_df.index.hour==15) & (stock_price_df.index.minute==30)]["Close"]
            temp_df.index=pd.to_datetime(temp_df.index).date
            benchmarks_df[stock]=temp_df[stock]
            temp_df=pd.DataFrame()

        benchmarks_df=benchmarks_df.dropna()
        
        benchmarks_df["SPY %"]=((benchmarks_df["SPY"]-benchmarks_df["SPY"][0])/benchmarks_df["SPY"][0])*100
        benchmarks_df["QQQ %"]=((benchmarks_df["QQQ"]-benchmarks_df["QQQ"][0])/benchmarks_df["QQQ"][0])*100
        benchmarks_df["Portfolio %"]=((benchmarks_df["Portfolio"]-benchmarks_df["Portfolio"][0])/benchmarks_df["Portfolio"][0])*100
        
        benchmarks_df.index=pd.to_datetime(benchmarks_df.index).date       
        benchmarks_df=benchmarks_df.dropna()
        
        return benchmarks_df
        
    def calculate_strategy_stats(self, startdate, enddate, balance_history_df, transactions_df):
        self.balance_history_df=balance_history_df
        self.transactions_df=transactions_df

        avg_win=transactions_df.loc[transactions_df['Net (%)']>0, 'Net (%)'].mean()
        avg_loss=transactions_df.loc[transactions_df['Net (%)']<0, 'Net (%)'].mean()
        winrate=len(transactions_df.loc[transactions_df['Net (%)']>0, 'Net (%)'])/len(transactions_df)*100
        totalprofit=transactions_df["Net ($)"].sum()
        ROR=abs(avg_win/avg_loss)   
        
        
        diffyears = enddate.year - startdate.year
        difference  = enddate - startdate.replace(enddate.year)
        days_in_year = isleap(enddate.year) and 366 or 365
        years = diffyears + (difference.days + difference.seconds/86400.0)/days_in_year
        
        beginning_balance=balance_history_df["Balance"].iloc[0]
        end_balance=balance_history_df["Balance"].iloc[-1]
        
        total_return=end_balance-beginning_balance
        total_return_perc=(end_balance-beginning_balance)/beginning_balance*100
        
        cagr=((end_balance/beginning_balance)**(1/years)-1)*100
        
        balance_history_df["Daily Returns"]=balance_history_df["Balance"].pct_change(1)
        trading_days=255
        riskfreerate=0.01
        mean=(balance_history_df["Daily Returns"].mean()*trading_days)-riskfreerate
        
        std_sharpe=balance_history_df["Daily Returns"].std()*(trading_days**0.5)
        sharpe=mean/std_sharpe
        
        balance_history_sortino_df=balance_history_df.loc[balance_history_df["Daily Returns"]<0]
        std_sortino=balance_history_sortino_df["Daily Returns"].std()*(trading_days**0.5)        
        sortino=mean/std_sortino
        
        balance_history_df["Comp_Ret"]=(balance_history_df["Daily Returns"]+1).cumprod()
        balance_history_df["Peak"]=balance_history_df["Comp_Ret"].expanding(min_periods=1).max()
        balance_history_df["DrawDown"]=(balance_history_df["Comp_Ret"]/balance_history_df["Peak"])-1
        max_drawdown=balance_history_df["DrawDown"].min()*100
        
        calmars=balance_history_df["Daily Returns"].mean()*trading_days/(abs(max_drawdown)/100)
        
        try:   
            print(f'Final Balance: ${end_balance:.2f}')  
            print(f'ROR: {ROR:.2f}')
            print(f'Win Rate: {winrate:.2f}%')       
            print(f"CAGR: {cagr:.2f}%")
            print(f"Total Return: {total_return_perc:.2f}%")
            print(f"Sharpe: {sharpe:.2f}")
            print(f"Sortino: {sortino:.2f}")
            print(f"Max Drawdown: {max_drawdown:.2f}%")
            print(f"Calmars: {calmars:.2f}")
        except:
            pass
        
        return cagr, total_return, total_return_perc, sharpe, max_drawdown
    
    def change_bar_interval(self, historical_stock_data_df, new_interval):
        self.historical_stock_data_df=historical_stock_data_df
        self.new_interval=new_interval
        
        historical_stock_data_df=historical_stock_data_df.groupby(pd.Grouper(freq=new_interval)).agg({"Open":"first",
                                                                                                      "Close":"last",
                                                                                                      "Low":"min",
                                                                                                      "High": "max",
                                                                                                      "Volume":"sum"})
        historical_stock_data_df.columns=["Open", "High", "Low", "Close", "Volume"]
        historical_stock_data_df=historical_stock_data_df.dropna()
        
        return (historical_stock_data_df)
    
    def combine_stock_data(self, stocks, startdate, enddate, type):
        self.stocks=stocks
        self.startdate=startdate
        self.enddate=enddate
        self.type=type
        
        all_historical_stock_price_df=pd.DataFrame()
        
        for stock in stocks:
            temp_historical_df=pd.DataFrame()
            
            historical_stock_price_df=self.get_historical_data(stock, startdate, enddate)
            
            temp_historical_df[stock]=historical_stock_price_df[type]
            
            all_historical_stock_price_df=all_historical_stock_price_df.merge(temp_historical_df, left_index=True, right_index=True, how='outer')
            
        return all_historical_stock_price_df
    
    def combine_stock_data_change_interval(self, stocks, startdate, enddate, type, bar_interval):
        self.stocks=stocks
        self.startdate=startdate
        self.enddate=enddate
        self.type=type
        self.bar_interval=bar_interval
        
        all_historical_stock_price_df=pd.DataFrame()
        
        for stock in stocks:
            temp_historical_df=pd.DataFrame()
            
            historical_stock_price_df=self.get_historical_data(stock, startdate, enddate)
            historical_stock_price_df=self.change_bar_interval(historical_stock_price_df, bar_interval)
            
            temp_historical_df[stock]=historical_stock_price_df[type]
            
            all_historical_stock_price_df=all_historical_stock_price_df.merge(temp_historical_df, left_index=True, right_index=True, how='outer')
            
        return all_historical_stock_price_df
       
    def get_historical_data(self, stock, startdate, enddate):
        self.stock=stock
        self.startdate=startdate
        self.enddate=enddate
        
        filename=stock+".csv"
        historical_stock_price_df=pd.read_csv("/Users/milligil/STOCK_DATABASE/PRICES/"+filename)
        historical_stock_price_df["Date"]=pd.to_datetime(historical_stock_price_df['Date'])
        historical_stock_price_df=historical_stock_price_df[::-1]
        historical_stock_price_df=historical_stock_price_df.set_index("Date")
        historical_stock_price_df=historical_stock_price_df.loc[startdate:enddate]
        historical_stock_price_df=historical_stock_price_df.between_time('09:00:00', "16:00:00")
        
        return historical_stock_price_df    
    
    def stoplosscheck(self, stock, price, open_positions_df):
        self.stock=stock
        self.price=price
        self.open_positions_df=open_positions_df
        
        stoplosslimit=open_positions_df.loc[stock, "Stop Loss ($)"]
        
        if self.price<=stoplosslimit:
            stoplosscheck_result="Yes"
        else:
            stoplosscheck_result="No"
            
        return stoplosscheck_result
    
    def stoploss_set(self, stock, price, stoplosslimit, trailing, trailing_loss_limit, open_positions_df):
        self.stock=stock
        self.price=price
        self.open_positions_df=open_positions_df
        self.stoplosslimit=stoplosslimit
        self.trailing=trailing
        self.trailing_loss_limit=trailing_loss_limit
        
        open_price=open_positions_df.loc[stock, "Price Bought ($)"]
        previous_stop_loss=open_positions_df.loc[stock, "Stop Loss ($)"]
        
        if trailing=="Yes":
            if self.price>open_price:
                if ((1-self.trailing_loss_limit)*self.price)>previous_stop_loss:
                    stoploss_current=(1-self.trailing_loss_limit)*self.price
                else:
                    stoploss_current=previous_stop_loss
            else:
                stoploss_current=(1-self.stoplosslimit)*open_price
        else:
            stoploss_current=(1-self.stoplosslimit)*open_price
            
        self.open_positions_df.loc[stock, "Stop Loss ($)"]=stoploss_current
        
        return self.open_positions_df
        
    def updatebalance(self, currentdate, open_positions_df, available_balance, balance_history_df):
        temp_open_balance=pd.DataFrame()
        
        self.currentdate=currentdate
        self.open_positions_df=open_positions_df
        self.available_balance=available_balance
        self.balance_history_df=balance_history_df
        
        temp_balance_history=[]
        d={}
        d["Date"]=currentdate
    
        temp_open_balance["Open Balance"]=open_positions_df["Shares"]*open_positions_df["Current Price ($)"]
        open_balance=temp_open_balance["Open Balance"].sum()
        d["Balance"]=available_balance+open_balance
        temp_balance_history.append(d)
        temp_balance_history=pd.DataFrame(temp_balance_history)
        balance_history_df=balance_history_df.append(temp_balance_history)
        return balance_history_df
    
    def updatebalance_no_open(self, currentdate, available_balance, balance_history_df):
        self.currentdate=currentdate
        self.available_balance=available_balance
        self.balance_history_df=balance_history_df
        
        temp_balance_history=[]
        d={}
        d["Date"]=currentdate
        d["Balance"]=available_balance
        temp_balance_history.append(d)
        temp_balance_history=pd.DataFrame(temp_balance_history)
        balance_history_df=balance_history_df.append(temp_balance_history)
        
        return balance_history_df
       
            
if __name__ == '__main__':          
        
    stocks=["AAPL", "MSFT"]
    start = "2019-07-01"
    end = "2022-12-27"
    type="Close"
    
    historical_stock_data=SimulatorFunctions().combine_stock_data(stocks, start, end, type)
    
    
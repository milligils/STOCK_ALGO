import pandas as pd

class Portfolio(object):
    def __init__(self):
        pass
        
    def stockbuy(self, date, stock, price, positionsize, available_balance, open_positions_df):
        trade_df=[]
        self.date=date
        self.stock=stock
        self.price=price
        self.positionsize=positionsize
        self.available_balance=available_balance
        self.open_positions_df=open_positions_df 
        
        shares_to_buy=int((self.available_balance*self.positionsize)/self.price)
        
        if shares_to_buy==0:
            print("Not enough money to buy: " + stock)

        else:
            self.available_balance-=(shares_to_buy*self.price)

            d={}
            d["Date Opened"]=self.date
            d["Stock"]=self.stock
            d["Shares"]=shares_to_buy
            d["Price Bought ($)"]=self.price
            d["Current Price ($)"]=self.price
            trade_df.append(d)
            trade_df=pd.DataFrame(trade_df)
            trade_df=trade_df.set_index("Stock")
            
            open_positions_df=self.open_positions_df.append(trade_df)
            
            #print(f"Bought {shares_to_buy} shares of {self.stock} at ${self.price:.2f} on {self.date}. Current available balance is ${self.available_balance:.2f}")
        
        return self.available_balance, open_positions_df
    
    def stocksell(self, open_positions_df, date, stock, price, available_balance):
        selltransaction_df=[]
        self.open_positions_df=open_positions_df
        self.date=date
        self.stock=stock
        self.price=price
        self.available_balance=available_balance

        shares_to_sell=open_positions_df.loc[stock, "Shares"]
        price_bought=open_positions_df.loc[stock, "Price Bought ($)"]
        date_bought=open_positions_df.loc[stock , "Date Opened"]
            
        self.available_balance+=(shares_to_sell*self.price)
        
        d={}
        d["Date Opened"]=date_bought
        d["Date Sold"]=date
        d["Stock"]=self.stock
        d["Shares"]=shares_to_sell
        d["Price Bought ($)"]=price_bought
        d["Price Sold ($)"]=self.price
        d["Net ($)"]=(self.price-price_bought)*shares_to_sell
        d["Net (%)"]=((self.price-price_bought)*shares_to_sell)/(price_bought*shares_to_sell)*100
        selltransaction_df.append(d)
        selltransaction_df=pd.DataFrame(selltransaction_df)
        
        open_positions_df=open_positions_df.drop(index=stock, axis=0)
        
        trade_result=abs((self.price-price_bought)*shares_to_sell)
        
        #if (self.price-price_bought)*shares_to_sell>0:
            #print(f"Sold {shares_to_sell} shares of {self.stock} at ${self.price:.2f} on {self.date} for a profit of ${trade_result:.2f}")
        #else:
            #print(f"Sold {shares_to_sell} shares of {self.stock} at ${self.price:.2f} on {self.date} for a loss of ${trade_result:.2f}")
        
        return self.available_balance, selltransaction_df, open_positions_df
        
if __name__ == '__main__':   
    #creating empty dataframes to store trades
    buys_df=pd.DataFrame(columns=["Date Opened", "Stock", "Shares", "Price Bought ($)"])
    transactions_df = pd.DataFrame(columns=["Date Opened", "Date Sold", "Stock", "Shares", "Price Bought ($)", "Price Sold ($)", "Net ($)", "Net (%)"])
    
    ex = {}
    ex["Stock"] = ["MSFT", "MSFT", "MSFT", "AAPL", "GME", "GE"]
    ex["Buydate"] = ["06-01-2022", "06-05-2022", "06-10-2022", "06-09-2022", "07-10-2022", "10-20-2022"]
    ex["Selldate"] = ["06-04-2022", "06-06-2022", "06-13-2022", "07-10-2022", "07-11-2022", "10-25-2022"]
    ex["Buyprice"] = [200, 255, 230, 141, 34, 12]
    ex["Sellprice"] = [350, 240, 270, 137, 50, 10]
    ex = pd.DataFrame(ex)
      
    available_balance = 10000
    positionsize = 0.05

    count = 0
    while count < (len(ex)):
        portfolio = Portfolio()
        stock = ex["Stock"][count]
        buydate = ex["Buydate"][count]
        selldate = ex["Selldate"][count]
        buyprice = ex["Buyprice"][count]
        sellprice = ex["Sellprice"][count]
                        
        stockbuy = portfolio.stockbuy(buydate, stock, buyprice, positionsize, available_balance)
        balance = stockbuy[0]
        buys_df = buys_df.append(stockbuy[1])

        stocksell = portfolio.stocksell(buys_df, selldate, stock, sellprice, available_balance)
        balance = stocksell[0]
        transactions_df = transactions_df.append(stocksell[1])
        count += 1
    
    pd.set_option('display.colheader_justify', 'center')
    print(transactions_df)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import finplot as fplt
import scipy.stats as st

stock="abnb"
stock=stock.upper()
filename=stock+".csv"

#4H intervals, bollinger bands converted to 8H to approximate 20D. 
sma_interval=2*4

sma_short_duration=20*sma_interval
sma_med_duration=50*sma_interval
sma_long_duration=200*sma_interval

historical_stock_price_df=pd.read_csv("/Users/milligil/STOCK_DATABASE/PRICES/"+filename)
historical_stock_price_df["Date"]=pd.to_datetime(historical_stock_price_df['Date'])
historical_stock_price_df=historical_stock_price_df.set_index("Date")
historical_stock_price_df=historical_stock_price_df[::-1]

historical_stock_price_df['SMA Short']=historical_stock_price_df["Close"].rolling(window=sma_short_duration).mean()
historical_stock_price_df['SMA Med']=historical_stock_price_df["Close"].rolling(window=sma_med_duration).mean()
historical_stock_price_df['SMA Long']=historical_stock_price_df["Close"].rolling(window=sma_long_duration).mean()
historical_stock_price_df["SMA Diff"]=(historical_stock_price_df["Close"]-historical_stock_price_df["SMA Long"])/historical_stock_price_df["SMA Long"]
historical_stock_price_df['Bollinger Upper']=historical_stock_price_df["Close"].rolling(window=sma_short_duration*2).mean()+historical_stock_price_df["Close"].rolling(window=sma_short_duration*2).std()
historical_stock_price_df['Bollinger Lower']=historical_stock_price_df["Close"].rolling(window=sma_short_duration*2).mean()-historical_stock_price_df["Close"].rolling(window=sma_short_duration*2).std()

sma_mean=historical_stock_price_df["SMA Diff"].mean()
sma_std=historical_stock_price_df["SMA Diff"].std()
historical_stock_price_df["SMA Diff Percentile"]=st.norm.cdf((historical_stock_price_df["SMA Diff"]-sma_mean)/sma_std)
    
print(sma_mean, sma_std)

open_prices=historical_stock_price_df["Open"].at_time('09:30')
close_prices=historical_stock_price_df["Close"].at_time('15:30')
#print(open_prices)
#print(close_prices)

#print(historical_stock_price_df)

plt.figure(figsize=(11,8))

plt.subplot(2,1,1)
plt.plot(historical_stock_price_df.index, historical_stock_price_df["SMA Long"], label="SMA200", color="red", linewidth=1)
plt.plot(historical_stock_price_df.index, historical_stock_price_df["SMA Med"], label="SMA50", color="orange", linewidth=1)
plt.plot(historical_stock_price_df.index, historical_stock_price_df["SMA Short"], label="SMA20", color="green", linewidth=1)
plt.plot(historical_stock_price_df.index, historical_stock_price_df["Close"], label="Price", color="blue", linewidth=1)
plt.plot(historical_stock_price_df.index, historical_stock_price_df["Bollinger Upper"], label="Bollinger Upper", color="purple", linewidth=1)
plt.plot(historical_stock_price_df.index, historical_stock_price_df["Bollinger Lower"], label="Bollinger Lower", color="purple", linewidth=1)

plt.title(stock+" Price ($)")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()

plt.subplot(2,1,2)
plt.plot(historical_stock_price_df.index, historical_stock_price_df["Volume"].rolling(window="7D").mean(), label="Weekly", color="red")
plt.plot(historical_stock_price_df.index, historical_stock_price_df["Volume"].rolling(window="365D").mean(), label="Yearly", color="navy")
plt.plot(historical_stock_price_df.index, historical_stock_price_df["Volume"].rolling(window="30D").mean(), label="Monthly", color="green")

plt.title("Volume")
plt.xlabel("Date")
plt.ylabel("Volume")
plt.legend()

plt.show()


plt.plot(historical_stock_price_df.index, historical_stock_price_df["SMA Diff"], label="Absolute SMA Difference", color="red", linewidth=1)
plt.show()

plt.plot(historical_stock_price_df.index, historical_stock_price_df["SMA Diff Percentile"], label="Absolute SMA Difference", color="red", linewidth=1)
plt.show()

plt.hist(historical_stock_price_df["SMA Diff"])
plt.show()
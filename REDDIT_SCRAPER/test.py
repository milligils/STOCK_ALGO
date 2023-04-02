import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import finplot as fplt
import scipy.stats as st

stock="GME"
filename=stock+".csv"

sma_short_duration=20
sma_med_duration=50
sma_long_duration=200

historical_stock_price_df=pd.read_csv("/Users/milligil/Desktop/STOCK_DATABASE/PRICES/"+filename)
historical_stock_price_df["Date"]=pd.to_datetime(historical_stock_price_df['Date'])
historical_stock_price_df=historical_stock_price_df[::-1]

historical_stock_price_df=historical_stock_price_df.set_index('Date')
#historical_stock_price_df=historical_stock_price_df[::-1]

close_prices=pd.DataFrame(historical_stock_price_df["Close"].at_time('15:30'))

reddit_mentions_df=pd.read_csv("/Users/milligil/Desktop/STOCK_DATABASE/REDDIT_MENTIONS/MASTER_REDDIT_MENTIONS.csv")
reddit_mentions_df["Date"]=reddit_mentions_df["Date"]+" 16:00:00"
reddit_mentions_df["Date"]=pd.to_datetime(reddit_mentions_df["Date"])
reddit_mentions_df=reddit_mentions_df.set_index("Date")


stock_mentions_df=pd.DataFrame(reddit_mentions_df[stock])
stock_mentions_df["SMA 1MO"]=stock_mentions_df[stock].rolling("30D").mean()
stock_mentions_df["SMA 1WK"]=stock_mentions_df[stock].rolling("7D").mean()
stock_mentions_df["SMA 6MO"]=stock_mentions_df[stock].rolling("180D").mean()

#print(stock_mentions_df, close_prices)

fig, ax1=plt.subplots()

ax1.set_xlabel("Date")
ax1.set_ylabel("Stock Price")
ax1.plot(close_prices.index, close_prices, color="blue", linewidth=1)

ax2=ax1.twinx()
ax2.set_ylabel("Mentions (per 10000 comments")
ax2.plot(stock_mentions_df.index, stock_mentions_df[stock], color="red", linewidth=1)
ax2.plot(stock_mentions_df.index, stock_mentions_df["SMA 1WK"], color="green", label="1WK", linewidth=1)
ax2.plot(stock_mentions_df.index, stock_mentions_df["SMA 1MO"], color="olive", label="1MO",linewidth=1)
ax2.plot(stock_mentions_df.index, stock_mentions_df["SMA 6MO"], color="black", label="6MO",linewidth=1)

plt.legend()
plt.show()



import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import scipy.stats as st

stock="abnb"
stock=stock.upper()
filename=stock+".csv"
percentile=1

historical_stock_price_df=pd.read_csv("/Users/milligil/STOCK_DATABASE/PRICES/"+filename)
historical_stock_price_df["Date"]=pd.to_datetime(historical_stock_price_df['Date'])

historical_stock_price_df=historical_stock_price_df.set_index('Date')

d={}
d["Open"]=historical_stock_price_df["Open"].at_time('09:00')
d["Close"]=historical_stock_price_df["Close"].at_time("15:30")
diff_df=pd.DataFrame(d)

#Good way to create daily stock dataframe.  You have to resample by day and remove NANs
diff_df=diff_df.resample("D").mean()
diff_df=diff_df.dropna()

diff_df["Daily Difference"]=(diff_df["Close"]-diff_df["Open"])/diff_df["Open"]*100
mean=diff_df["Daily Difference"].mean()
stdev=diff_df["Daily Difference"].std()

diff_df["Percentile"]=st.norm.cdf((diff_df["Daily Difference"]-mean)/stdev)*100

diff_df["1 Day Return"]=(-diff_df["Close"].diff(periods=-1))/diff_df["Close"]*100
diff_df["2 Day Return"]=(-diff_df["Close"].diff(periods=-2))/diff_df["Close"]*100
diff_df["3 Day Return"]=(-diff_df["Close"].diff(periods=-3))/diff_df["Close"]*100
diff_df["4 Day Return"]=(-diff_df["Close"].diff(periods=-4))/diff_df["Close"]*100
diff_df["5 Day Return"]=(-diff_df["Close"].diff(periods=-5))/diff_df["Close"]*100
diff_df["6 Day Return"]=(-diff_df["Close"].diff(periods=-6))/diff_df["Close"]*100
diff_df["7 Day Return"]=(-diff_df["Close"].diff(periods=-7))/diff_df["Close"]*100
diff_df["8 Day Return"]=(-diff_df["Close"].diff(periods=-8))/diff_df["Close"]*100
diff_df["9 Day Return"]=(-diff_df["Close"].diff(periods=-9))/diff_df["Close"]*100
diff_df["10 Day Return"]=(-diff_df["Close"].diff(periods=-10))/diff_df["Close"]*100
diff_df["15 Day Return"]=(-diff_df["Close"].diff(periods=-15))/diff_df["Close"]*100
diff_df["20 Day Return"]=(-diff_df["Close"].diff(periods=-20))/diff_df["Close"]*100

print(np.percentile(diff_df["Daily Difference"], percentile))
print(len(diff_df.loc[diff_df["Percentile"]<percentile]))
check=diff_df.loc[diff_df["Percentile"]<percentile]
results_df=[]

d={}
percentWin_1d=len(check.loc[check["1 Day Return"]>0])/len(check)
avgwin_1d=check.loc[check["1 Day Return"]>0].mean()
avgloss_1d=check.loc[check["1 Day Return"]<0].mean()
d["Days Out"]="1"
d["Win Percent"]=percentWin_1d
d["Avg. Win (%)"]=avgwin_1d["1 Day Return"]
d["Avg. Loss (%)"]=avgloss_1d["1 Day Return"]
results_df.append(d)
d={}

percentWin_2d=len(check.loc[check["2 Day Return"]>0])/len(check)
avgwin_2d=check.loc[check["2 Day Return"]>0].mean()
avgloss_2d=check.loc[check["2 Day Return"]<0].mean()
d["Days Out"]="2"
d["Win Percent"]=percentWin_2d
d["Avg. Win (%)"]=avgwin_2d["2 Day Return"]
d["Avg. Loss (%)"]=avgloss_2d["2 Day Return"]
results_df.append(d)
d={}

percentWin_3d=len(check.loc[check["3 Day Return"]>0])/len(check)
avgwin_3d=check.loc[check["3 Day Return"]>0].mean()
avgloss_3d=check.loc[check["3 Day Return"]<0].mean()
d["Days Out"]="3"
d["Win Percent"]=percentWin_3d
d["Avg. Win (%)"]=avgwin_3d["3 Day Return"]
d["Avg. Loss (%)"]=avgloss_3d["3 Day Return"]
results_df.append(d)
d={}

percentWin_4d=len(check.loc[check["4 Day Return"]>0])/len(check)
avgwin_4d=check.loc[check["4 Day Return"]>0].mean()
avgloss_4d=check.loc[check["4 Day Return"]<0].mean()
d["Days Out"]="4"
d["Win Percent"]=percentWin_4d
d["Avg. Win (%)"]=avgwin_4d["4 Day Return"]
d["Avg. Loss (%)"]=avgloss_4d["4 Day Return"]
results_df.append(d)
d={}

percentWin_5d=len(check.loc[check["5 Day Return"]>0])/len(check)
avgwin_5d=check.loc[check["5 Day Return"]>0].mean()
avgloss_5d=check.loc[check["5 Day Return"]<0].mean()
d["Days Out"]="5"
d["Win Percent"]=percentWin_5d
d["Avg. Win (%)"]=avgwin_5d["5 Day Return"]
d["Avg. Loss (%)"]=avgloss_5d["5 Day Return"]
results_df.append(d)
d={}

percentWin_6d=len(check.loc[check["6 Day Return"]>0])/len(check)
avgwin_6d=check.loc[check["6 Day Return"]>0].mean()
avgloss_6d=check.loc[check["6 Day Return"]<0].mean()
d["Days Out"]="6"
d["Win Percent"]=percentWin_6d
d["Avg. Win (%)"]=avgwin_6d["6 Day Return"]
d["Avg. Loss (%)"]=avgloss_6d["6 Day Return"]
results_df.append(d)
d={}

percentWin_7d=len(check.loc[check["7 Day Return"]>0])/len(check)
avgwin_7d=check.loc[check["7 Day Return"]>0].mean()
avgloss_7d=check.loc[check["7 Day Return"]<0].mean()
d["Days Out"]="7"
d["Win Percent"]=percentWin_7d
d["Avg. Win (%)"]=avgwin_7d["7 Day Return"]
d["Avg. Loss (%)"]=avgloss_7d["7 Day Return"]
results_df.append(d)
d={}

percentWin_8d=len(check.loc[check["8 Day Return"]>0])/len(check)
avgwin_8d=check.loc[check["8 Day Return"]>0].mean()
avgloss_8d=check.loc[check["8 Day Return"]<0].mean()
d["Days Out"]="8"
d["Win Percent"]=percentWin_8d
d["Avg. Win (%)"]=avgwin_8d["8 Day Return"]
d["Avg. Loss (%)"]=avgloss_8d["8 Day Return"]
results_df.append(d)
d={}

percentWin_9d=len(check.loc[check["9 Day Return"]>0])/len(check)
avgwin_9d=check.loc[check["9 Day Return"]>0].mean()
avgloss_9d=check.loc[check["9 Day Return"]<0].mean()
d["Days Out"]="9"
d["Win Percent"]=percentWin_9d
d["Avg. Win (%)"]=avgwin_9d["9 Day Return"]
d["Avg. Loss (%)"]=avgloss_9d["9 Day Return"]
results_df.append(d)
d={}

percentWin_10d=len(check.loc[check["10 Day Return"]>0])/len(check)
avgwin_10d=check.loc[check["10 Day Return"]>0].mean()
avgloss_10d=check.loc[check["10 Day Return"]<0].mean()
d["Days Out"]="10"
d["Win Percent"]=percentWin_10d
d["Avg. Win (%)"]=avgwin_10d["10 Day Return"]
d["Avg. Loss (%)"]=avgloss_10d["10 Day Return"]
results_df.append(d)
d={}

percentWin_15d=len(check.loc[check["15 Day Return"]>0])/len(check)
avgwin_15d=check.loc[check["15 Day Return"]>0].mean()
avgloss_15d=check.loc[check["15 Day Return"]<0].mean()
d["Days Out"]="15"
d["Win Percent"]=percentWin_15d
d["Avg. Win (%)"]=avgwin_15d["15 Day Return"]
d["Avg. Loss (%)"]=avgloss_15d["15 Day Return"]
results_df.append(d)
d={}

percentWin_20d=len(check.loc[check["20 Day Return"]>0])/len(check)
avgwin_20d=check.loc[check["20 Day Return"]>0].mean()
avgloss_20d=check.loc[check["20 Day Return"]<0].mean()
d["Days Out"]="20"
d["Win Percent"]=percentWin_20d
d["Avg. Win (%)"]=avgwin_20d["20 Day Return"]
d["Avg. Loss (%)"]=avgloss_20d["20 Day Return"]
results_df.append(d)
d={}

results_df.append(d)
results_df=pd.DataFrame(results_df)
#results_df=results_df.dropna()
results_df["ROR"]=abs(results_df["Avg. Win (%)"]/results_df["Avg. Loss (%)"])
print(results_df)




fig, ax1=plt.subplots()
ax1.scatter(diff_df["Percentile"], diff_df["1 Day Return"], color="blue")
#ax1.scatter(diff_df["Percentile"], diff_df["2 Day Return"], color="green")
#ax1.scatter(diff_df["Percentile"], diff_df["3 Day Return"], color="orange")
ax1.scatter(diff_df["Percentile"], diff_df["5 Day Return"], color="red")
#ax1.scatter(diff_df["Percentile"], diff_df["20 Day Return"], color="teal")

plt.title(stock+" Changes")
plt.xlabel("Percentile")
plt.ylabel("1 Day Change (%)")
plt.show()

import pandas as pd
import numpy as np
import pandas_market_calendars as mycal
from datetime import timedelta, datetime, date
import matplotlib.pyplot as plt
from scipy import stats

currentdate = datetime(2020, 4, 1)
#enddate = datetime(2020, 4, 30).strftime('%Y-%m-%d')
enddate=date.today().strftime('%Y-%m-%d')

nyse=mycal.get_calendar('NYSE')
calendar=nyse.schedule(start_date="2020-01-01", end_date="2022-12-31")
calendar=mycal.date_range(calendar,frequency="1D")
calendar=calendar.strftime('%Y-%m-%d')

final_mentions_df=[]
mentions_df=[]
while currentdate.strftime('%Y-%m-%d') != enddate:
    if currentdate.strftime('%Y-%m-%d') in calendar: 
        
        filename=currentdate.strftime('%Y-%m-%d')+".csv"
        try:
            current=pd.read_csv("/Users/milligil/Desktop/STOCK_DATABASE/REDDIT_MENTIONS/SCRAPES/"+filename)
            daily_comments=current["Total Comments"][0]
            daily_stocks=current["Symbol"]
            
            d={}
            d["Date"]=currentdate
            d["Daily Comments"]=daily_comments
            
            count=0
            for stock in daily_stocks:
                mentions=current["Mentions"][count]
                mentions_corrected=(mentions*10000)/daily_comments
                d[stock]=mentions_corrected
                mentions_df.append(mentions_corrected)
                count+=1
                
            final_mentions_df.append(d)
            
        except:
            #print(currentdate.strftime('%Y-%m-%d')+" was not found")
            pass
        
    currentdate=currentdate+timedelta(days=1)

mentions_df=np.log(mentions_df)
final_mentions_df=pd.DataFrame(final_mentions_df) 
mentions_df=pd.DataFrame(mentions_df)


#ex=final_mentions_df["MSFT"]
#ex=np.log(ex)
#fitted_data, fitted_lambda = stats.boxcox(ex)
#print(fitted_lambda)

#fitted_data=pd.DataFrame(fitted_data)


#ax=mentions_df.plot.hist( bins=50)
#plt.show()
 
final_mentions_df=final_mentions_df.fillna(0)

cols_to_keep=["Date", "Daily Comments"]
other_cols=np.sort(final_mentions_df.columns.difference(cols_to_keep)).tolist()
final_mentions_df=final_mentions_df.loc[:, cols_to_keep+other_cols]

filename="MASTER_REDDIT_MENTIONS.csv"
final_mentions_df.to_csv("/Users/milligil/Desktop/STOCK_DATABASE/REDDIT_MENTIONS/"+filename, index=False)  

print(final_mentions_df) 
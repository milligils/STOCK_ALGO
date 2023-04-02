import pandas as pd
import numpy as np
from GET_STOCK_DATA import StockInfo as si
from datetime import date, timedelta, datetime
import pandas_market_calendars as mycal

today=date.today().strftime("%Y-%m-%d")
filename="TOTAL_STOCK_LIST.csv"
stocks=pd.read_csv("/Users/milligil/STOCK_DATABASE/"+filename)
stocks=stocks.Symbol.tolist()
#stocks=["TSLA", "MSFT"]

start= datetime(2023, 3, 26)
end=datetime(2023, 4, 1)
#start=today
#end=today
#start="2017-11-05"
#end="2017-12-05"

period_poly=5
periodtype_poly="minute"
date_advance=90

timerlength=int(np.floor(len(stocks)/10))
counter=1

#nyse=mycal.get_calendar('NYSE')
#calendar=nyse.schedule(start_date="2020-01-01", end_date="2022-12-31")
#calendar=mycal.date_range(calendar,frequency="1D")
#calendar=calendar.strftime('%Y-%m-%d')

for stock in stocks:
    filename=(str(stock)+".csv")
    current_start=start
    data=pd.DataFrame()
    
    while current_start < end:    
        current_end=current_start+timedelta(days=date_advance)
        if current_end>end:
            current_end=end   
             
        try:
            temp_data=si().get_prices_polygon(stock, period_poly, periodtype_poly, current_start, current_end)
            #temp_data["Date"]=temp_data["Date"].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
            temp_data['Date']=temp_data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
            if len(data)<1:
                data=temp_data
            else:
                data=[temp_data, data]
                data=pd.concat(data)
            
        except:
            print(f'{stock} did not work on {current_start}')
            pass
        
        current_start=current_end  
    
    try:
        previous_data=pd.read_csv("/Users/milligil/STOCK_DATABASE/PRICES/"+filename)
        #previous_data=pd.read_csv("/Users/milligil/STOCK_DATABASE/PRICES2/"+filename)
        #previous_data=pd.read_csv("MUSIC_IAN/STOCK_DATABASE/PRICES2/"+filename)
        previous_data["Date"]=pd.to_datetime(previous_data["Date"])

        data=pd.concat([previous_data, data])
        data["Date"]=pd.to_datetime(data["Date"])
        
    except:
        pass
    
    try:
        data=data.sort_values(by="Date", ascending=False)
        data.reset_index(inplace=True)
        del data["index"]
        data=data.drop_duplicates()
        data.to_csv("/Users/milligil/STOCK_DATABASE/PRICES/"+filename, index=False)
        #data.to_csv("/Users/milligil/STOCK_DATABASE/PRICES2/"+filename, index=False)
        #data.to_csv("MUSIC_IAN/STOCK_DATABASE/PRICES2/"+filename, index=False)
        
    except:
        pass    
    
    if len(stocks)>10:        
        if counter % timerlength==0:
            print(str(int(counter/timerlength*10))+"%"+ " Complete")
        counter+=1

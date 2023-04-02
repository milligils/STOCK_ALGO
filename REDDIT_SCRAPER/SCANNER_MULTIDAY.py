from reddit_scraper import Scraper
import pandas_market_calendars as mycal
from datetime import timedelta, datetime, date

currentdate = datetime(2022, 12, 9)
enddate="2022-12-17"
#enddate=date.today().strftime('%Y-%m-%d')

nyse=mycal.get_calendar('NYSE')
calendar=nyse.schedule(start_date="2020-01-01", end_date="2022-12-31")
calendar=mycal.date_range(calendar,frequency="1D")
calendar=calendar.strftime('%Y-%m-%d')

while currentdate.strftime('%Y-%m-%d') != enddate:
    if currentdate.strftime('%Y-%m-%d') in calendar: 
        s=Scraper(currentdate)
        s.get_comments()
    currentdate=currentdate+timedelta(days=1) 
    


